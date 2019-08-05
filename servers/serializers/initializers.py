import os

if os.environ.get('API_RESOURCE') == 'pod':
    from .pod import *
else:
    raise Exception('API_RESOURCE environment variable not assigned or invalid.')
