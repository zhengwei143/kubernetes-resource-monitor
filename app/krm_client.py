import requests
from kubernetes import client

class KRMClient():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = 'http://{}:{}'.format(host, port)

    def get_pods(self, namespace=None, node=None, label_selector=None):
        url = '{}/pods'.format(self.url)
        params = {
            'namespace': namespace,
            'node': node,
            'label_selector': label_selector
        }
        response = requests.get(url=url, params=params)
        print(response.text)
