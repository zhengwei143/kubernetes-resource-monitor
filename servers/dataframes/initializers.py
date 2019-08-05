import os
from .pod import *
from kubernetes_api_client import api_client

def initialize_dataframe(schema_generator):
    schema = schema_generator()
    columns = schema.keys()
    df = pd.DataFrame(data=[], columns=columns)
    return df.astype(dtype=schema)

def initialize_aggregated_schema():
    api_resource = os.environ.get('API_RESOURCE')
    if api_resource == 'pod':
        return pod_aggregated_schema()

    raise Exception('API_RESOURCE environment variable not assigned.')

def initialize_streamed_schema():
    api_resource = os.environ.get('API_RESOURCE')
    if api_resource == 'pod':
        return pod_streamed_schema()

    raise Exception('API_RESOURCE environment variable not assigned.')

def initialize_verified_schema():
    api_resource = os.environ.get('API_RESOURCE')
    if api_resource == 'pod':
        return pod_verified_schema()

    raise Exception('API_RESOURCE environment variable not assigned.')


def build_entry(type, name, namespace, **kwargs):
    if type == 'streamed':
        base_obj = initialize_streamed_schema()
        suffix = '_streamed'
    elif type == 'verified':
        base_obj = initialize_verified_schema()
        suffix = '_verified'
    elif type == 'aggregated':
        base_obj = initialize_aggregated_schema()
        suffix = ''
    # Set all values to None
    base_obj = dict((key, None) for key in base_obj.keys())
    base_obj['name'] = name
    base_obj['namespace'] = namespace

    for key, value in kwargs.items():
        if key == 'object' and type != 'aggregated':
            value = api_client.sanitize_for_serialization(value)
            value.pop('apiVersion', None)
            value.pop('kind', None)
        base_obj['{}{}'.format(key, suffix)] = value
    return base_obj
