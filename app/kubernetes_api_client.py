import os
from kubernetes import client

config = client.Configuration()
config.host = os.environ.get('CLUSTER_ENDPOINT')
config.verify_ssl = False
config.api_key = { "authorization": "Bearer " + os.environ.get('TOKEN') }

api_client = client.ApiClient(config)
api = client.CoreV1Api(api_client)
extensions_api = client.ExtensionsV1beta1Api(api_client)

def watching_namespaced_resource():
    non_namespaced_resources = ['node']
    return os.environ.get('API_RESOURCE') not in non_namespaced_resources

if os.environ.get('API_RESOURCE') == 'pod':
    api_query = api.list_pod_for_all_namespaces
elif os.environ.get('API_RESOURCE') == 'pvc':
    api_query = api.list_persistent_volume_claim_for_all_namespaces
elif os.environ.get('API_RESOURCE') == 'node':
    api_query = api.list_node
elif os.environ.get('API_RESOURCE') == 'service':
    api_query = api.list_service_for_all_namespaces
elif os.environ.get('API_RESOURCE') == 'ingress':
    api_query = extensions_api.list_ingress_for_all_namespaces
elif os.environ.get('API_RESOURCE') == 'deployment':
    api_query = extensions_api.list_deployment_for_all_namespaces
else:
    raise Exception('API_RESOURCE environment variable not assigned or invalid.')
