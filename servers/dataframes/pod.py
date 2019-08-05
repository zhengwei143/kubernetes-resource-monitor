from .base import *

pod_additional_columns = {
    'memory': 'object',
    'cpu': 'object',
    'gpu': 'object'
}

def initialize_aggregated_schema():
    return aggregated_schema(**pod_additional_columns)

def initialize_streamed_schema():
    return streamed_schema(**pod_additional_columns)

def initialize_verified_schema():
    return verified_schema(**pod_additional_columns)
