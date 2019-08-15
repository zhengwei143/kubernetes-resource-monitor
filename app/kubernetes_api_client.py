import os
from kubernetes import client

config = client.Configuration()
config.host = os.environ.get('CLUSTER_ENDPOINT')
config.verify_ssl = False
config.api_key = { "authorization": "Bearer " + os.environ.get('TOKEN') }

api_client = client.ApiClient(config)
api = client.CoreV1Api(api_client)
extensions_api = client.ExtensionsV1beta1Api(api_client)

def api_query():
    if os.environ.get('API_RESOURCE') == 'pod':
        return api.list_pod_for_all_namespaces()
    elif os.environ.get('API_RESOURCE') == 'pvc':
        return api.list_persistent_volume_claim_for_all_namespaces()
    elif os.environ.get('API_RESOURCE') == 'node':
        return api.list_node()
    elif os.environ.get('API_RESOURCE') == 'service':
        return api.list_service_for_all_namespaces()
    elif os.environ.get('API_RESOURCE') == 'ingress':
        return extensions_api.list_ingress_for_all_namespaces()
    elif os.environ.get('API_RESOURCE') == 'deployment':
        return extensions_api.list_deployment_for_all_namespaces()
    else:
        raise Exception('API_RESOURCE environment variable not assigned or invalid.')
