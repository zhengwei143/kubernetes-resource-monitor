import os
import pandas as pd
from kubernetes_api_client import api_client

def initialize_dataframe(schema_generator):
    schema = schema_generator()
    columns = schema.keys()
    df = pd.DataFrame(data=[], columns=columns)
    return df.astype(dtype=schema)

if os.environ.get('API_RESOURCE') == 'pod':
    from .pod import initialize_streamed_schema, initialize_verified_schema, initialize_aggregated_schema
else:
    raise Exception('API_RESOURCE environment variable not assigned or invalid.')


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
