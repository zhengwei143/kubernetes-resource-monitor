from .base import *

pod_additional_columns = {
    'memory': 'object',
    'cpu': 'object',
    'gpu': 'object'
}

def pod_aggregated_schema():
    return aggregated_schema(**pod_additional_columns)

def pod_streamed_schema():
    return streamed_schema(**pod_additional_columns)

def pod_verified_schema():
    return verified_schema(**pod_additional_columns)
