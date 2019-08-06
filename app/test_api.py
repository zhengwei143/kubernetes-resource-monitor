from krm_client import KRMClient

if __name__ == '__main__':
    host = "0.0.0.0"
    port = 8003

    krm_client = KRMClient(host, port)
    krm_client.get_pods(namespace='default', node='sgw0007')
