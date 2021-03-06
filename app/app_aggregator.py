import os
import asyncio
import pandas as pd
from redis_store import *
from utils.helpers import *
from dataframes.initializers import *
from serializers.initializers import serialize_aggregated

# Takes grouped events/pods from JOINED stream and verified data and returns the updated pod
def aggregate_subframe(df):
    # Aggregate here and return a single row dataframe
    df = df.sort_values(by=['resource_version_verified', 'resource_version_streamed'], ascending=False)
    latest_event = df.iloc[0]
    if str(latest_event['event_streamed']) == Event.deleted:
        return None

    if cmp_resource_version_dtype(latest_event['resource_version_verified'], latest_event['resource_version_streamed']):
        return serialize_aggregated(latest_event, 'streamed')
    else:
        return serialize_aggregated(latest_event, 'verified')


API_RESOURCE = os.environ.get('API_RESOURCE')

async def aggregate(streamed_data, verified_data):
    merge_columns = ['namespace', 'name']
    # Certain resources are not namespaced and should not be merged on the namespace column
    if not watching_namespaced_resource():
        merge_columns = ['name']
    matched_records = pd.merge(verified_data, streamed_data, on=merge_columns, how='outer')
    print_dataframe(streamed_data, name='Streamed Dataframe')
    print_dataframe(verified_data, name='Verified Dataframe')
    print_dataframe(matched_records, name='Matched Dataframe')

    aggregated_data = initialize_dataframe(initialize_aggregated_schema)

    for (merge_columns, subframe) in matched_records.groupby(merge_columns):
        aggregated_data = aggregated_data.append(aggregate_subframe(subframe), ignore_index=True)

    print_dataframe(aggregated_data, name='Aggregated Dataframe')
    store_dataframe(get_key(API_RESOURCE, 'aggregated'), aggregated_data)

aggregation_wait_duration = int(os.environ.get('AGGREGATION_WAIT_DURATION', 0))

async def schedule_aggregation():
    while True:
        stream_key = get_key(API_RESOURCE, 'streamed')
        verified_key = get_key(API_RESOURCE, 'verified')
        if not redis_connection.exists(stream_key) or not redis_connection.exists(verified_key):
            print('Streaming data and verification data not ready.')
            await asyncio.sleep(5)
            continue

        streamed_data = retrieve_dataframe(get_key(API_RESOURCE, 'streamed'))
        verified_data = retrieve_dataframe(get_key(API_RESOURCE, 'verified'))

        await aggregate(streamed_data, verified_data)
        await asyncio.sleep(aggregation_wait_duration)

if __name__ == '__main__':
    # Aggregator should not persist the dataframe
    df = initialize_dataframe(initialize_aggregated_schema)
    store_dataframe(get_key(API_RESOURCE, 'aggregated'), df)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(schedule_aggregation())
    finally:
        loop.close()
