import pandas as pd
from dataframes.initializers import build_entry
from utils.helpers import *

def serialize_streamed(object, event, stable):
    pvcs = []
    if object.spec.volumes:
        for volume in object.spec.volumes:
            pvc = volume.persistent_volume_claim
            pvcs.append(pvc.claim_name) if pvc else None
    resources = pod_resources_requested(object)
    return build_entry(
        'streamed',
        name=object.metadata.name,
        namespace=object.metadata.namespace,
        resource_version=float(object.metadata.resource_version),
        labels=object.metadata.labels,
        event=event,
        node=object.spec.node_name,
        memory=resources.get('memory'),
        cpu=resources.get('cpu'),
        gpu=resources.get('gpu'),
        pvcs=tuple(pvcs),
        object=object,
        time=datetime_now(),
        stable=stable
    )

def serialize_verified(object):
    pvcs = []
    if object.spec.volumes:
        for volume in object.spec.volumes:
            pvc = volume.persistent_volume_claim
            pvcs.append(pvc.claim_name) if pvc else None
    resources = pod_resources_requested(object)
    return build_entry(
        'verified',
        name=object.metadata.name,
        namespace=object.metadata.namespace,
        resource_version=float(object.metadata.resource_version),
        labels=object.metadata.labels,
        node=object.spec.node_name,
        memory=resources.get('memory'),
        cpu=resources.get('cpu'),
        gpu=resources.get('gpu'),
        pvcs=tuple(pvcs),
        object=object
    )

def serialize_aggregated(latest_event, type):
    resource_version, labels, object, node, memory, cpu, gpu, pvcs = extract_values(latest_event, type)
    return build_entry(
        'aggregated',
        name=latest_event['name'],
        namespace=latest_event['namespace'],
        labels=labels,
        resource_version=resource_version,
        node=node,
        memory=memory,
        cpu=cpu,
        gpu=gpu,
        pvcs=pvcs,
        object=object
    )

def extract_values(event, type):
    return (
        event['resource_version_{}'.format(type)],
        event['labels_{}'.format(type)],
        event['object_{}'.format(type)],
        event['node_{}'.format(type)],
        event['memory_{}'.format(type)],
        event['cpu_{}'.format(type)],
        event['gpu_{}'.format(type)],
        event['pvcs_{}'.format(type)]
    )
