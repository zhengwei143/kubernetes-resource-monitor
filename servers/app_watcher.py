import asyncio
import urllib3
import pandas as pd
from kubernetes import client, watch
from redis_store import *
from kubernetes_api_client import api
from utils.helpers import *
from watchers.pod import *
from dataframes.pod import pod_streamed_schema
from dataframes.initializers import initialize_dataframe, build_entry

def serialize(object, event):
    resources = pod_resources_requested(object)
    return build_entry(
        'streamed',
        name=object.metadata.name,
        namespace=object.metadata.namespace,
        resource_version=float(object.metadata.resource_version),
        event=event,
        node=object.spec.node_name,
        memory=resources.get('memory'),
        cpu=resources.get('cpu'),
        gpu=resources.get('gpu'),
        object=object
    )

def update_redis_dataframe(event):
    """ Serializes a Kubernetes Event and inserts or updates
    a row in the pandas dataframe stored in redis
    """
    pod = event['object']
    df = serialize(pod, event=event['type'])

    existing_df = retrieve_dataframe(STREAM_KEY)
    existing_entry = existing_df.loc[
            (existing_df['name'] == pod.metadata.name) &
            (existing_df['namespace'] == pod.metadata.namespace)
        ]

    # Ignore identical entries (pods) with the same or older resource version
    most_recent_rv = existing_entry['resource_version_streamed'].max()
    current_rv = int(pod.metadata.resource_version)
    if not existing_entry.empty and not to_update_resource_version(most_recent_rv, current_rv):
        return

    updated_df = existing_df.append(df, ignore_index=True)
    print_dataframe(updated_df, name='Updated Dataframe')
    store_dataframe(STREAM_KEY, updated_df)


async def watch_cluster(handler=lambda x: None):
    resource_version = ""
    while True:
        event_watch = watch.Watch()
        print("Resource Version: {}".format(resource_version))
        stream = event_watch.stream(
            api.list_pod_for_all_namespaces,
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
    # if not redis_connection.exists(STREAM_KEY):
    if True:
        df = initialize_dataframe(pod_streamed_schema)
        store_dataframe(STREAM_KEY, df)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(watch_cluster())
    finally:
        loop.close()
