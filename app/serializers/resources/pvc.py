import pandas as pd
from dataframes.initializers import build_entry
from utils.helpers import *

def serialize_streamed(object, event, stable):
    return build_entry(
        'streamed',
        name=object.metadata.name,
        namespace=object.metadata.namespace,
        resource_version=float(object.metadata.resource_version),
        labels=object.metadata.labels,
        event=event,
        storage_class=object.spec.storage_class_name,
        object=object,
        time=datetime_now(),
        stable=stable
    )

def serialize_verified(object):
    return build_entry(
        'verified',
        name=object.metadata.name,
        namespace=object.metadata.namespace,
        resource_version=float(object.metadata.resource_version),
        labels=object.metadata.labels,
        storage_class=object.spec.storage_class_name,
        object=object
    )

def serialize_aggregated(latest_event, type):
    resource_version, labels, object, storage_class = extract_values(latest_event, type)
    return build_entry(
        'aggregated',
        name=latest_event['name'],
        namespace=latest_event['namespace'],
        labels=labels,
        resource_version=resource_version,
        storage_class=storage_class,
        object=object
    )

def extract_values(event, type):
    return (
        event['resource_version_{}'.format(type)],
        event['labels_{}'.format(type)],
        event['object_{}'.format(type)],
        event['storage_class_{}'.format(type)]
    )
