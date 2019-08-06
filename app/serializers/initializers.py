import os

if os.environ.get('API_RESOURCE') == 'pod':
    from .resources.pod import *
elif os.environ.get('API_RESOURCE') == 'pvc':
    from .resources.pvc import *
elif os.environ.get('API_RESOURCE') == 'node':
    from .resources.node import *
elif os.environ.get('API_RESOURCE') == 'service':
    from .resources.service import *
elif os.environ.get('API_RESOURCE') == 'ingress':
    from .resources.ingress import *
elif os.environ.get('API_RESOURCE') == 'deployment':
    from .resources.deployment import *
else:
    raise Exception('API_RESOURCE environment variable not assigned or invalid.')
