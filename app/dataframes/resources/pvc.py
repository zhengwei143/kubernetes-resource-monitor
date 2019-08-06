from .base import *

pvc_additional_columns = {
    'storage_class': 'object',
}

def initialize_aggregated_schema():
    return aggregated_schema(**pvc_additional_columns)

def initialize_streamed_schema():
    return streamed_schema(**pvc_additional_columns)

def initialize_verified_schema():
    return verified_schema(**pvc_additional_columns)
