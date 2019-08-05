import os
import json
import redis as r
import pandas as pd
from kubernetes import utils

STREAM_KEY = 'streamed_data'
VERIFIED_KEY = 'verified_data'
AGGREGATED_KEY = 'aggregated_data'

redis_connection = r.Redis(
    host=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    password=os.environ.get('REDIS_PASSWORD')
)

def store_dataframe(key, dataframe):
    msg_pack = dataframe.to_msgpack(compress='zlib')
    redis_connection.set(key, msg_pack)

def retrieve_dataframe(key):
    msg_pack = redis_connection.get(key)
    return pd.read_msgpack(msg_pack)


class Event:
    error = 'ERROR'
    added = 'ADDED'
    deleted = 'DELETED'
    modified = 'MODIFIED'

def deserialize(object, api_client):
    # api client expects to deserialize a REST response
    class Response():
        """ Wrapper object to mimic REST Response """
        def __init__(self, data):
            self.data = data

    return api_client.deserialize(Response(json.dumps(sanitized)), 'V1Pod')
