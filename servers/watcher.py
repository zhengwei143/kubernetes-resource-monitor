import os
import asyncio
import urllib3
from kubernetes import client, watch
from db.redis_store import *

config = client.Configuration()
config.host = os.environ.get('CLUSTER_ENDPOINT')
config.verify_ssl = False
config.api_key = { "authorization": "Bearer " + os.environ.get('TOKEN') }
api_client = client.ApiClient(config)
api = client.CoreV1Api(api_client)
STREAM_KEY = 'streamed_data'

def update_redis_dataframe(event, api_client):
    """ Serializes a Kubernetes Event and inserts or updates
    a row in the pandas dataframe stored in redis
    """
    if event['type'] == Event.error:
        return

    pod = event['object']
    df = serialize(pod, api_client)
    existing_df = retrieve_dataframe(STREAM_KEY)
    existing_entry = existing_df.loc[
            (existing_df['pod_name'] == pod.metadata.name) &
            (existing_df['namespace'] == pod.metadata.namespace)
        ]

    updated_df = existing_df
    if not existing_entry.empty:
        # Only update existing entries if the resource_version is larger, and ignore objects otherwise
        if to_update_resource_version(existing_entry['resource_version'], pod.metadata.resource_version):
            if event['type'] == Event.deleted:
                print("Deleting entry: {}".format(existing_entry['pod_name']))
                print(updated_df)
                updated_df.drop(existing_entry.index, inplace=True)
                print("Deleted entry:")
                print(updated_df)
            else: # Modify existing
                existing_entry = df
    else:
        if event['type'] == Event.deleted:
            # Should not be happening
            print("Delete event on non existent entry found: \n", df)
            return

        updated_df = existing_df.append(df, ignore_index=True)
    store_dataframe(STREAM_KEY, updated_df)

async def watch_cluster():
    resource_version = ""
    while True:
        event_watch = watch.Watch()
        stream = event_watch.stream(
            api.list_pod_for_all_namespaces,
            resource_version=resource_version,
            timeout_seconds=5
        )
        try:
            for event in stream:
                resource_version = event['object'].metadata.resource_version or ''
                update_redis_dataframe(event, api_client)
        except Exception as error:
            print("An error occurred, restarting event stream: {}".format(error))
        finally:
            event_watch.stop()


if __name__ == '__main__':
    if not redis_connection.exists(STREAM_KEY):
        df = initialize_dataframe()
        store_dataframe(STREAM_KEY, df)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(watch_cluster())
    finally:
        loop.close()
