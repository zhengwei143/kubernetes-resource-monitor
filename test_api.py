from client.krm_client import KRMClient

if __name__ == '__main__':
    host = "krm-api"
    port = 80

    krm_client = KRMClient(host, port)
    pods = krm_client.get_pods(namespace='default', node='sgw0007')
    # print(pods)
    nodes = krm_client.get_nodes()
    # print(nodes)
    services = krm_client.get_services(name='armory-zhengweitan', namespace='default')
    # print(services)
    ingress = krm_client.get_ingress(name='armory-zhengweitan', namespace='default')
    # print(ingress)
    pvcs = krm_client.get_pvcs(namespace='default')
    # print(pvcs)
    deployments = krm_client.get_deployments(label_selector='k8s-app=armory-zhengweitan')
    # print(deployments)
