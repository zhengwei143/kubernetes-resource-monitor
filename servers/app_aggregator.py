import os
import asyncio
import pandas as pd
from redis_store import *
from utils.helpers import *
from dataframes.pod import pod_aggregated_schema
from dataframes.initializers import initialize_dataframe, build_entry

async def aggregate():
    merge_columns = ['namespace', 'name']
    streamed_data = retrieve_dataframe(STREAM_KEY)
    verified_data = retrieve_dataframe(VERIFIED_KEY)
    matched_records = pd.merge(verified_data, streamed_data, on=merge_columns, how='outer')
    print(matched_records.dtypes)
    print_dataframe(streamed_data, name='Streamed Dataframe')
    print_dataframe(verified_data, name='Verified Dataframe')
    print_dataframe(matched_records, name='Matched Dataframe')

    aggregated_data = initialize_dataframe(pod_aggregated_schema)

    for ((namespace, name), subframe) in matched_records.groupby(merge_columns):
        # print_dataframe(subframe, name='Subframe [namespace] {} [name] {}'.format(namespace, name))
        aggregated_data = aggregated_data.append(aggregate_subframe(subframe), ignore_index=True)

    print_dataframe(aggregated_data, name='Aggregated Dataframe')
    store_dataframe(AGGREGATED_KEY, aggregated_data)

# Takes grouped events/pods from JOINED stream and verified data and returns the updated pod
def aggregate_subframe(df):
    # Aggregate here and return a single row dataframe
    df = df.sort_values(by=['resource_version_verified', 'resource_version_streamed'], ascending=False)
    latest_event = df.iloc[0]
    if str(latest_event['event_streamed']) == Event.deleted:
        return None

    if cmp_resource_version_dtype(latest_event['resource_version_verified'], latest_event['resource_version_streamed']):
        resource_version, object, node, memory, cpu, gpu = extract_values(latest_event, 'streamed')
    else:
        resource_version, object, node, memory, cpu, gpu = extract_values(latest_event, 'verified')

    return build_entry(
        'aggregated',
        name=latest_event['name'],
        namespace=latest_event['namespace'],
        resource_version=resource_version,
        node=node,
        memory=memory,
        cpu=cpu,
        gpu=gpu,
        object=object
    )

async def schedule_aggregation():
    while True:
        await aggregate()
        await asyncio.sleep(30)

if __name__ == '__main__':
    # if not redis_connection.exists(AGGREGATED_KEY):
    if True:
        df = initialize_dataframe(pod_aggregated_schema)
        store_dataframe(AGGREGATED_KEY, df)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(schedule_aggregation())
    finally:
        loop.close()
