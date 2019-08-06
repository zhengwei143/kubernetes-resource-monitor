import pandas as pd

def aggregated_schema(**kwargs):
    return {
        'name': 'object',
        'namespace': 'object',
        'resource_version': 'object',
        'node': 'object',
        **kwargs,
        'object': 'object',
    }

def streamed_schema(**kwargs):
    updated_kwargs = dict(('{}_streamed'.format(key), value) for key, value in kwargs.items())
    return {
        'event_streamed': 'object',
        'name': 'object',
        'namespace': 'object',
        'resource_version_streamed': 'float64',
        'node_streamed': 'object',
        **updated_kwargs,
        # 'object_streamed': 'object'
    }

def verified_schema(**kwargs):
    updated_kwargs = dict(('{}_verified'.format(key), value) for key, value in kwargs.items())
    return {
        'name': 'object',
        'namespace': 'object',
        'resource_version_verified': 'float64',
        'node_verified': 'object',
        **updated_kwargs,
        'object_verified': 'object'
    }
