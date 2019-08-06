from .base import *

node_additional_columns = {}

def initialize_aggregated_schema():
    return aggregated_schema(**node_additional_columns)

def initialize_streamed_schema():
    return streamed_schema(**node_additional_columns)

def initialize_verified_schema():
    return verified_schema(**node_additional_columns)
