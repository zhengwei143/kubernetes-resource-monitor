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

    def deserialize_json(self, json_object_list, type):
        # api client expects to deserialize a REST response
        class Wrapper():
            """ Wrapper object to mimic REST Response """
            def __init__(self, data):
                self.data = data

        return self.api_client.deserialize(Wrapper(json_object_list), type)

    def get_pods(self, name=None, namespace=None, node=None, label_selector=None):
        params = {
            'name': name,
            'namespace': namespace,
            'node': node,
            'label_selector': label_selector
        }
        response = requests.get(url=self.get_url('/pods'), params=params)
        return self.deserialize_json(response.text, 'V1PodList')

    def get_nodes(self):
        response = requests.get(url=self.get_url('/nodes'))
        return self.deserialize_json(response.text, 'V1NodeList')

    def get_services(self, name=None, namespace=None, label_selector=None):
        params = {
            'name': name,
            'namespace': namespace,
            'label_selector': label_selector
        }
        response = requests.get(url=self.get_url('/services'), params=params)
        return self.deserialize_json(response.text, 'V1ServiceList')

    def get_ingress(self, name=None, namespace=None, label_selector=None):
        params = {
            'name': name,
            'namespace': namespace,
            'label_selector': label_selector
        }
        response = requests.get(url=self.get_url('/ingress'), params=params)
        return self.deserialize_json(response.text, 'ExtensionsV1beta1IngressList')

    def get_pvcs(self, name=None, namespace=None, label_selector=None):
        params = {
            'name': name,
            'namespace': namespace,
            'label_selector': label_selector
        }
        response = requests.get(url=self.get_url('/pvcs'), params=params)
        return self.deserialize_json(response.text, 'V1PersistentVolumeClaimList')

    def get_deployments(self, name=None, namespace=None, label_selector=None):
        params = {
            'name': name,
            'namespace': namespace,
            'label_selector': label_selector
        }
        response = requests.get(url=self.get_url('/deployments'), params=params)
        return self.deserialize_json(response.text, 'ExtensionsV1beta1DeploymentList')
