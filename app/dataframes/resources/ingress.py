from .base import *

ingress_additional_columns = {}

def initialize_aggregated_schema():
    return aggregated_schema(**ingress_additional_columns)

def initialize_streamed_schema():
    return streamed_schema(**ingress_additional_columns)

def initialize_verified_schema():
    return verified_schema(**ingress_additional_columns)
