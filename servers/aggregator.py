import os
import asyncio
import pandas as pd
from db.redis_store import *
from utils.helpers import *

async def aggregate():
    merge_columns = ['namespace', 'pod_name']
    streamed_data = retrieve_dataframe(STREAM_KEY)
    verified_data = retrieve_dataframe(VERIFIED_KEY)
    matched_records = pd.merge(verified_data, streamed_data, on=merge_columns, how='outer')
    print_dataframe(streamed_data, name='Streamed Dataframe')
    print_dataframe(verified_data, name='Verified Dataframe')

    # rv_x_nan = matched_records[matched_records['resource_version_x'].isnull()]
    # print_dataframe(rv_x_nan, 'resource_version_x is Nan')
    # rv_y_nan = matched_records[matched_records['resource_version_y'].isnull()]
    # print_dataframe(rv_y_nan, 'resource_version_y is Nan')
    # rv_ne = matched_records[matched_records['resource_version_x'] != matched_records['resource_version_y']]
    # print_dataframe(rv_ne, 'resource_version_xy not equal')
    print_dataframe(matched_records, name='Matched Dataframe')

    aggregated_data = initialize_dataframe()

    for ((namespace, pod_name), subframe) in matched_records.groupby(merge_columns):
        # print_dataframe(subframe, name='Subframe [namespace] {} [pod_name] {}'.format(namespace, pod_name))
        aggregated_data = aggregated_data.append(aggregate_subframe(subframe), ignore_index=True)

    print_dataframe(aggregated_data, name='Aggregated Dataframe')
    store_dataframe(AGGREGATED_KEY, aggregated_data)

# Takes grouped events/pods from JOINED stream and verified data and returns the updated pod
def aggregate_subframe(df):
    # Aggregate here and return a single row dataframe
    df['resource_version_x'] = df['resource_version_x'].astype('float')
    df['resource_version_y'] = df['resource_version_y'].astype('float')
    df = df.sort_values(by=['resource_version_x', 'resource_version_y'], ascending=False)
    most_recent_event = df.iloc[0]
    if str(most_recent_event['event']) == Event.deleted:
        return None

    rv_verified, rv_streamed = most_recent_event['resource_version_x'], most_recent_event['resource_version_y']
    obj_verified, obj_streamed = most_recent_event['object_x'], most_recent_event['object_y']

    if rv_verified < rv_streamed:
        resource_version = rv_streamed
        object = obj_streamed
    else:
        resource_version = rv_verified
        object = obj_verified

    return {
        'pod_name': most_recent_event['pod_name'],
        'namespace': most_recent_event['namespace'],
        'resource_version': resource_version,
        'node': most_recent_event['node_x'],
        'object': object
    }

async def schedule_aggregation():
    while True:
        await aggregate()
        await asyncio.sleep(30)

def initialize_dataframe():
    columns = ['pod_name', 'namespace', 'resource_version', 'node', 'object']
    return pd.DataFrame(data=[], columns=columns)

if __name__ == '__main__':
    # if not redis_connection.exists(AGGREGATED_KEY):
    if True:
        df = initialize_dataframe()
        store_dataframe(AGGREGATED_KEY, df)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(schedule_aggregation())
    finally:
        loop.close()
