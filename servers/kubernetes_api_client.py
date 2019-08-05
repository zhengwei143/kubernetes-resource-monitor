import os
from kubernetes import client

config = client.Configuration()
config.host = os.environ.get('CLUSTER_ENDPOINT')
config.verify_ssl = False
config.api_key = { "authorization": "Bearer " + os.environ.get('TOKEN') }

api_client = client.ApiClient(config)
api = client.CoreV1Api(api_client)
