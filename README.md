# Kubernetes Resource Monitor

An application used to cache existing resources on a Kubernetes cluster, with the goal of providing an alternative to making repeated requests directly to the Kubernetes API server.
The caching mechanism aims to reduce the delays in obtaining resources from the API server as the cache is continuously updated via a stream.

### Current resources:
1. Pods
2. Deployments
3. Persistent Volume Claims
4. Services
5. Ingress
6. Nodes
