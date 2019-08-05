import os
import asyncio
import urllib3
import pandas as pd
from kubernetes import watch
from redis_store import *
from kubernetes_api_client import api
from utils.helpers import *
from dataframes.pod import pod_verified_schema
from dataframes.initializers import initialize_dataframe, build_entry

def serialize(object):
    resources = pod_resources_requested(object)
    return build_entry(
        'verified',
        name=object.metadata.name,
        namespace=object.metadata.namespace,
        resource_version=float(object.metadata.resource_version),
        node=object.spec.node_name,
        memory=resources.get('memory'),
        cpu=resources.get('cpu'),
        gpu=resources.get('gpu'),
        object=object
    )

async def verify_cluster():
    comparable_columns = ['name', 'namespace', 'resource_version_verified', 'node']
    verified_df = initialize_dataframe(pod_verified_schema)
    pods = api.list_pod_for_all_namespaces()
    for pod in pods.items:
        df = serialize(pod)
        verified_df = verified_df.append(df, ignore_index=True)

    print_dataframe(verified_df, name='Verified Dataframe')
    store_dataframe(VERIFIED_KEY, verified_df)


async def schedule_verification():
    while True:
        await verify_cluster()
        print("Done verifying dataframes...")
        await asyncio.sleep(30)

if __name__ == '__main__':
    # if not redis_connection.exists(VERIFIED_KEY):
    if True:
        df = initialize_dataframe(pod_verified_schema)
        store_dataframe(VERIFIED_KEY, df)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(schedule_verification())
    finally:
        loop.close()
