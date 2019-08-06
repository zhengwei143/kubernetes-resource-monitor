from .base import *

deployment_additional_columns = {}

def initialize_aggregated_schema():
    return aggregated_schema(**deployment_additional_columns)

def initialize_streamed_schema():
    return streamed_schema(**deployment_additional_columns)

def initialize_verified_schema():
    return verified_schema(**deployment_additional_columns)
