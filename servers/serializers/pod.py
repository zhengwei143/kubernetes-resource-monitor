import pandas as pd
from redis_store import *
from dataframes.initializers import build_entry
from utils.helpers import *

def serialize_streamed(object, event):
    resources = pod_resources_requested(object)
    return build_entry(
        'streamed',
        name=object.metadata.name,
        namespace=object.metadata.namespace,
        resource_version=float(object.metadata.resource_version),
        event=event,
        node=object.spec.node_name,
        memory=resources.get('memory'),
        cpu=resources.get('cpu'),
        gpu=resources.get('gpu'),
        object=object
    )

def serialize_verified(object):
    resources = pod_resources_requested(object)
    return build_entry(
        'verified',
        name=object.metadata.name,
        namespace=object.metadata.namespace,
        resource_version=float(object.metadata.resource_version),
        node=object.spec.node_name,
        memory=resources.get('memory'),
        cpu=resources.get('cpu'),
        gpu=resources.get('gpu'),
        object=object
    )

def serialize_aggregated(latest_event, type):
    resource_version, object, node, memory, cpu, gpu = extract_values(latest_event, type)
    return build_entry(
        'aggregated',
        name=latest_event['name'],
        namespace=latest_event['namespace'],
        resource_version=resource_version,
        node=node,
        memory=memory,
        cpu=cpu,
        gpu=gpu,
        object=object
    )
