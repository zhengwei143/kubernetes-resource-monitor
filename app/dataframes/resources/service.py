from .base import *

service_additional_columns = {}

def initialize_aggregated_schema():
    return aggregated_schema(**service_additional_columns)

def initialize_streamed_schema():
    return streamed_schema(**service_additional_columns)

def initialize_verified_schema():
    return verified_schema(**service_additional_columns)
