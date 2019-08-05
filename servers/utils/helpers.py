import math

def print_dataframe(df, name=''):
    if 'resource_version_streamed' in df.columns and 'resource_version_verified' in df.columns:
        sorted_df = df.sort_values(by=['namespace', 'name', 'resource_version_streamed', 'resource_version_verified'])
    elif 'resource_version_streamed' in df.columns:
        sorted_df = df.sort_values(by=['namespace', 'name', 'resource_version_streamed'])
    elif 'resource_version_verified' in df.columns:
        sorted_df = df.sort_values(by=['namespace', 'name', 'resource_version_verified'])
    else:
        sorted_df = df.sort_values(by=['namespace', 'name'])

    sorted_df = sorted_df.reset_index(drop=True)
    print('\n========================================== Dataframe: {} =========================================='.format(name))
    print(sorted_df)

def extract_values(event, type):
    if type == 'verified':
        return (
            event['resource_version_verified'],
            event['object_verified'],
            event['node_verified'],
            event['memory_verified'],
            event['cpu_verified'],
            event['gpu_verified']
        )
    elif type == 'streamed':
        return (
            event['resource_version_streamed'],
            event['object_streamed'],
            event['node_streamed'],
            event['memory_streamed'],
            event['cpu_streamed'],
            event['gpu_streamed']
        )

# Calculates the amount of resources requested by the pod
def pod_resources_requested(pod):
    containers = pod.spec.containers
    memory = 0
    cpu = 0
    gpu = 0

    for container in pod.spec.containers:
        resources = container.resources.requests
        if resources:
            memory += parse_bytes(resources.get('memory'))
            cpu += parse_cores(resources.get('cpu'))
            gpu += parse_gpus(resources.get('nvidia.com/gpu'))

    return {
        'memory': display_bytes(memory),
        'cpu': display_cores(cpu),
        'gpu': display_gpus(gpu)
    }

def to_update_resource_version(existing_rv, event_rv):
    if not event_rv:
        return False
    if not existing_rv:
        return True
    return int(existing_rv) < int(event_rv)

# Checks if left is less than right
def cmp_resource_version_dtype(left, right):
    if math.isnan(left) and math.isnan(right):
        return False
    elif math.isnan(left):
        return True
    elif math.isnan(right):
        return False
    return float(left) < float(right)

# Parses memory units: byte string to Gi
def parse_bytes(bytes_string, case=False):
	try:
		value = float(re.match(r'(\d*[.eE])?\d+', bytes_string).group(0))
		if not case:
			bytes_string = bytes_string.lower()
		if bytes_string.endswith('ki') or bytes_string.endswith('Ki'):
			return value / (2**20)
		elif bytes_string.endswith('mi') or bytes_string.endswith('Mi'):
			return value / (2**10)
		elif bytes_string.endswith('gi') or bytes_string.endswith('Gi'):
			return value
		elif bytes_string.endswith('M'):
			return value * (10**6) / (2**30)
		elif bytes_string.endswith('m'):
			if case:
				return value / (2**30) / (10 ** 3)
			return value * (10**6) / (2**30)
		elif bytes_string.endswith('g') or bytes_string.endswith('G'):
			return value * (10**9) / (2**30)
		elif bytes_string.endswith('ti') or bytes_string.endswith('Ti'):
			return value * 2**20
		elif bytes_string.endswith('pi') or bytes_string.endswith('Pi'):
			return value * 2**30
		else:
			return value
	except Exception as e:
		return 0

# Displays memory (bytes in Gi) in the next lowest unit
def display_bytes(bytes):
	if not bytes and bytes != 0:
		return ''
	if bytes >= 1 or bytes == 0:
		return '{}Gi'.format(round(bytes, 2))
	elif bytes >= 1 / (2**10):
		return '{}Mi'.format(round(bytes * (2**10), 2))
	return '{}Ki'.format(round(bytes * (2**20), 1))

# Parses cpu units: cores / millicores
def parse_cores(cores_string):
	try:
		value = float(re.match(r'(\d*[.eE])?\d+', cores_string).group(0))
		if 'm' in cores_string.lower():
			return value / 1000
		return value
	except Exception:
		return 0

# Displays cores in the next lowest unit
def display_cores(cores):
	if not cores and cores != 0:
		return None
	if 0 < cores < 1:
		return '{}m'.format(round(cores * 1000, 3))
	return '{}'.format(round(cores, 1))

def parse_gpus(gpu_string):
	try:
		value = float(re.match(r'(\d*[.eE])?\d+', gpu_string).group(0))
		return int(value)
	except Exception:
		return 0

def display_gpus(gpus):
	if not gpus and gpus != 0:
		return None
	return str(gpus)

def display_resource(resource, value):
	if resource == 'memory':
		return display_bytes(parse_bytes(value))
	elif resource == 'cpu':
		return display_cores(parse_cores(value))
	elif resource == 'gpu':
		return display_gpus(parse_gpus(value))
	return None
