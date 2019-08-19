import asyncio
import urllib3
import pandas as pd
from kubernetes import watch
from redis_store import *
from kubernetes_api_client import *
from utils.helpers import *
from dataframes.initializers import *
from serializers.initializers import serialize_streamed

API_RESOURCE = os.environ.get('API_RESOURCE')

def analyze_stable_event(event, time_streamed):
    if event['type'] == Event.modified:
        return
    obj = event['object']
    occurred_dt = extract_event_occurred_datetime(event)
    observed_dt = time_streamed
    if occurred_dt:
        print('{} {} {} {} {}'.format(event['type'], obj.metadata.name, obj.metadata.namespace, obj.metadata.resource_version, obj.metadata.uid))
        print("Occurred: ", occurred_dt)
        print("Observed: ", observed_dt)
        print("Diff: ", (observed_dt - occurred_dt))

def extract_event_occurred_datetime(event):
    if event['type'] == Event.added:
        return event['object'].metadata.creation_timestamp
    elif event['type'] == Event.deleted:
        return event['object'].metadata.deletion_timestamp
    return None

def update_redis_dataframe(event, stable):
    """ Serializes a Kubernetes Event and inserts or updates
    a row in the pandas dataframe stored in redis
    """
    obj = event['object']
    df = serialize_streamed(obj, event=event['type'], stable=stable)

    stream_key = get_key(API_RESOURCE, 'streamed')
    existing_df = retrieve_dataframe(stream_key)
    existing_entry = existing_df.loc[
            (existing_df['name'] == obj.metadata.name) &
            (existing_df['namespace'] == obj.metadata.namespace)
        ]

    # Ignore identical events with the same or older resource version
    most_recent_rv = existing_entry['resource_version_streamed'].max()
    current_rv = int(obj.metadata.resource_version)
    if not existing_entry.empty and not to_update_resource_version(most_recent_rv, current_rv):
        return

    if stable:
        analyze_stable_event(event, df['time_streamed'])

    updated_df = existing_df.append(df, ignore_index=True)
    print_dataframe(updated_df, name='Updated Dataframe')
    store_dataframe(stream_key, updated_df)

def parse_too_old_failure(message):
    regex = r"too old resource version: .* \((.*)\)"
    result = re.search(regex, message)
    if result == None:
        return None

    match = result.group(1)
    if match == None:
        return None

    try:
        return int(match)
    except:
        return None

async def watch_cluster(latest_resource_version):
    resource_version = latest_resource_version
    stream_stable = False
    while True:
        print("Requesting new stream with resource Version: {}".format(resource_version))
        event_watch = watch.Watch()
        received_old_event = False
        stream = event_watch.stream(
            api_query,
            resource_version=resource_version,
            timeout_seconds=5
        )
        try:
            for event in stream:
                # Usually event resource_version too old error
                if event['type'] == Event.error:
                    obj = event["raw_object"]
                    code = obj.get("code")
                    if code == 410:
                        new_version = parse_too_old_failure(obj.get("message"))
                        if not new_version:
                            resource_version = new_version
                            event_watch.resource_version = new_version

                print("Received event from stream: {} {} {} {}".format(
                    event['type'],
                    event['object'].metadata.name or '',
                    event['object'].metadata.namespace or '',
                    event['object'].metadata.resource_version or ''
                ))
                event_resource_version = event['object'].metadata.resource_version
                if to_update_resource_version(resource_version, event_resource_version):
                    resource_version = event_resource_version
                else:
                    received_old_event = True
                update_redis_dataframe(event, stable=stream_stable)

            if not received_old_event:
                stream_stable = True
        except Exception as error:
            print("An error occurred, restarting event stream: {}".format(error))
        finally:
            event_watch.stop()

if __name__ == '__main__':
    if not redis_connection.exists(get_key(API_RESOURCE, 'streamed')):
        print("Creating initial dataframe...")
        df = initialize_dataframe(initialize_streamed_schema)
        store_dataframe(get_key(API_RESOURCE, 'streamed'), df)
        latest_resource_version = ''
    else:
        df = retrieve_dataframe(get_key(API_RESOURCE, 'streamed'))
        latest_resource_version = str(int(df['resource_version_streamed'].max()))

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(watch_cluster(latest_resource_version))
    except Exception as error:
        print("Error in async: {}".format(error))
    finally:
        print("Exited async loop!")
        loop.close()
