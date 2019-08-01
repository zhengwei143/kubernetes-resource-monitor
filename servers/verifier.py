import os
import asyncio
import urllib3
import pandas as pd
from kubernetes import client, watch
from pandas.util.testing import assert_frame_equal
from db.redis_store import *

config = client.Configuration()
config.host = os.environ.get('CLUSTER_ENDPOINT')
config.verify_ssl = False
config.api_key = { "authorization": "Bearer " + os.environ.get('TOKEN') }
api_client = client.ApiClient(config)
api = client.CoreV1Api(api_client)
VERIFIED_KEY = 'verified_data'

async def verify_cluster():
    comparable_columns = ['pod_name', 'namespace', 'resource_version', 'node']
    verified_df = initialize_dataframe()
    pods = api.list_pod_for_all_namespaces()
    for pod in pods.items:
        df = serialize(pod, api_client)
        verified_df = verified_df.append(df, ignore_index=True)

    store_dataframe(VERIFIED_KEY, verified_df)
    # verified_df = verified_df.sort_values(by=['namespace', 'pod_name'])
    # print("Verifying Cluster, awaiting lock...")
    # with redis_connection.lock('lock'):
    #     print("Lock accessed, verifying cluster now...")
    #     existing_df = retrieve_dataframe()
    #     existing_df = existing_df.sort_values(by=['namespace', 'pod_name']).reset_index(drop=True)
    #     merged = pd.merge(verified_df, existing_df, on=comparable_columns, how='inner')
    #     if verified_df[comparable_columns].equals(existing_df[comparable_columns]):
    #         print("================== DFs are equal ==================")
    #         print(verified_df[comparable_columns])
    #     else:
    #         print("================== DFs are not equal ==================")
    #         print("Expected: \n", verified_df[comparable_columns])
    #         print("Actual: \n", existing_df[comparable_columns])

        # await asyncio.sleep(120)


async def schedule_verification():
    while True:
        await verify_cluster()
        print("Done verifying dataframes...")
        await asyncio.sleep(30)


if __name__ == '__main__':
    if not redis_connection.exists(VERIFIED_KEY):
        df = initialize_dataframe()
        store_dataframe(VERIFIED_KEY, df)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(schedule_verification())
    finally:
        loop.close()
