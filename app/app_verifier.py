import os
import asyncio
import urllib3
import pandas as pd
from kubernetes import watch
from redis_store import *
from kubernetes_api_client import *
from utils.helpers import *
from dataframes.initializers import *
from serializers.initializers import serialize_verified

API_RESOURCE = os.environ.get('API_RESOURCE')

def verify_cluster():
    comparable_columns = ['name', 'namespace', 'resource_version_verified', 'node']
    verified_df = initialize_dataframe(initialize_verified_schema)
    objects = api_query()
    for object in objects.items:
        df = serialize_verified(object)
        verified_df = verified_df.append(df, ignore_index=True)

    print_dataframe(verified_df, name='Verified Dataframe')
    store_dataframe(get_key(API_RESOURCE, 'verified'), verified_df)

verification_wait_duration = int(os.environ.get('VERIFICATION_WAIT_DURATION', 30))

async def schedule_verification():
    while True:
        verify_cluster()
        print("Done verifying dataframes...")
        await asyncio.sleep(verification_wait_duration)

if __name__ == '__main__':
    # if not redis_connection.exists(get_key(API_RESOURCE, 'verified')):
    if True:
        df = initialize_dataframe(initialize_verified_schema)
        store_dataframe(get_key(API_RESOURCE, 'verified'), df)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(schedule_verification())
    finally:
        loop.close()
