import json
import requests
import pandas as pd
from kubernetes import client

class KRMClient():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        config = client.Configuration()
        config.verify_ssl = False
        self.api_client = client.ApiClient(config)
        self.url = 'http://{}:{}'.format(host, port)

    def get_url(self, path):
        return '{}{}'.format(self.url, path)

    def deserialize(self, dataframe, type):
        print(dataframe)
        # api client expects to deserialize a REST response
        class Wrapper():
            """ Wrapper object to mimic REST Response """
            def __init__(self, data):
                self.data = json.dumps(data)

        deserialized_objects = []
        for object in dataframe['object']:
            deserialized_objects.append(self.api_client.deserialize(Wrapper(object), type))

        return deserialized_objects

    def get_pods(self, name=None, namespace=None, node=None, label_selector=None):
        params = {
            'name': name,
            'namespace': namespace,
            'node': node,
            'label_selector': label_selector
        }
        response = requests.get(url=self.get_url('/pods'), params=params)
        dataframe = pd.DataFrame(json.loads(response.text))
        return self.deserialize(dataframe, 'V1Pod')

    def get_nodes(self):
        response = requests.get(url=self.get_url('/nodes'))
        dataframe = pd.DataFrame(json.loads(response.text))
        return self.deserialize(dataframe, 'V1Node')

    def get_services(self, name=None, namespace=None, label_selector=None):
        params = {
            'name': name,
            'namespace': namespace,
            'label_selector': label_selector
        }
        response = requests.get(url=self.get_url('/services'), params=params)
        dataframe = pd.DataFrame(json.loads(response.text))
        return self.deserialize(dataframe, 'V1Service')

    def get_ingress(self, name=None, namespace=None, label_selector=None):
        params = {
            'name': name,
            'namespace': namespace,
            'label_selector': label_selector
        }
        response = requests.get(url=self.get_url('/ingress'), params=params)
        dataframe = pd.DataFrame(json.loads(response.text))
        return self.deserialize(dataframe, 'ExtensionsV1beta1Ingress')

    def get_pvcs(self, name=None, namespace=None, label_selector=None):
        params = {
            'name': name,
            'namespace': namespace,
            'label_selector': label_selector
        }
        response = requests.get(url=self.get_url('/pvcs'), params=params)
        dataframe = pd.DataFrame(json.loads(response.text))
        return self.deserialize(dataframe, 'V1PersistentVolumeClaim')

    def get_deployments(self, name=None, namespace=None, label_selector=None):
        params = {
            'name': name,
            'namespace': namespace,
            'label_selector': label_selector
        }
        response = requests.get(url=self.get_url('/deployments'), params=params)
        dataframe = pd.DataFrame(json.loads(response.text))
        return self.deserialize(dataframe, 'ExtensionsV1beta1Deployment')
