import asyncio
import urllib3
import pandas as pd
from kubernetes import client, watch
from redis_store import *
from kubernetes_api_client import *
from utils.helpers import *
from dataframes.initializers import *
from serializers.initializers import serialize_streamed

API_RESOURCE = os.environ.get('API_RESOURCE')

def update_redis_dataframe(event):
    """ Serializes a Kubernetes Event and inserts or updates
    a row in the pandas dataframe stored in redis
    """
    pod = event['object']
    df = serialize_streamed(pod, event=event['type'])

    existing_df = retrieve_dataframe(get_key(API_RESOURCE, 'streamed'))
    existing_entry = existing_df.loc[
            (existing_df['name'] == pod.metadata.name) &
            (existing_df['namespace'] == pod.metadata.namespace)
        ]

    # Ignore identical events with the same or older resource version
    most_recent_rv = existing_entry['resource_version_streamed'].max()
    current_rv = int(pod.metadata.resource_version)
    if not existing_entry.empty and not to_update_resource_version(most_recent_rv, current_rv):
        return

    updated_df = existing_df.append(df, ignore_index=True)
    print_dataframe(updated_df, name='Updated Dataframe')
    store_dataframe(get_key(API_RESOURCE, 'streamed'), updated_df)

async def watch_cluster():
    resource_version = ""
    while True:
        event_watch = watch.Watch()
        print("Resource Version: {}".format(resource_version))
        stream = event_watch.stream(
            api_query,
            resource_version=resource_version,
            timeout_seconds=5
        )
        try:
            for event in stream:
                # Usually event resource_version too old error
                if event['type'] == Event.error:
                    continue
                event_resource_version = event['object'].metadata.resource_version
                if to_update_resource_version(resource_version, event_resource_version):
                    resource_version = event['object'].metadata.resource_version
                update_redis_dataframe(event)
        except Exception as error:
            print("An error occurred, restarting event stream: {}".format(error))
        finally:
            event_watch.stop()


if __name__ == '__main__':
    # if not redis_connection.exists(get_key(API_RESOURCE, 'streamed')):
    if True:
        df = initialize_dataframe(initialize_streamed_schema)
        store_dataframe(get_key(API_RESOURCE, 'streamed'), df)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(watch_cluster())
    finally:
        loop.close()
