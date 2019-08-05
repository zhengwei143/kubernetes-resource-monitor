import os
from kubernetes import client

config = client.Configuration()
config.host = os.environ.get('CLUSTER_ENDPOINT')
config.verify_ssl = False
config.api_key = { "authorization": "Bearer " + os.environ.get('TOKEN') }

api_client = client.ApiClient(config)
api = client.CoreV1Api(api_client)

if os.environ.get('API_RESOURCE') == 'pod':
    api_query = api.list_pod_for_all_namespaces
elif os.environ.get('API_RESOURCE') == 'pvc':
    api_query = api.list_persistent_volume_claim_for_all_namespaces
else:
    raise Exception('API_RESOURCE environment variable not assigned or invalid.')
