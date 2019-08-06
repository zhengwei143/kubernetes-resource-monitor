import os
import json
import redis as r
import pandas as pd
from kubernetes import utils

def get_key(resource, type='aggregated'):
    valid_resources = ['pod', 'pvc', 'node', 'service', 'ingress']
    valid_types = ['aggregated', 'streamed', 'verified']
    if resource not in valid_resources or type not in valid_types:
        raise Exception('Invalid resource or type requested.')
    return '{}_{}_data'.format(resource, type)

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
