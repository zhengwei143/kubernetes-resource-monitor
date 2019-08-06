def equals(val, column_val):
    return val == column_val

def in_collection(val, column_collection):
    return val in column_collection

def in_dictionary(key_value_pair, column_dictionary):
    key, value = key_value_pair
    return key in column_dictionary and column_dictionary[key] == value

def generate_column_filter(column_name, value, comparator=equals):
    return lambda df: comparator(value, df[column_name])

def generate_node_filter(node_name):
    return generate_column_filter('node', node_name)

def generate_namespace_filter(namespace):
    return generate_column_filter('namespace', namespace)

def generate_contains_pvc_filter(pvc_name):
    return generate_column_filter('pvcs', pvc_name, comparator=in_collection)

def generate_label_selector_filter(label_selector):
    key_value_pair = tuple(label_selector.split('='))
    return generate_column_filter('labels', key_value_pair, comparator=in_dictionary)

def get_filter_generator(key):
    valid_filters = {
        'namespace': generate_namespace_filter,
        'node': generate_node_filter,
        'label_selector': generate_label_selector_filter
    }
    if key not in valid_filters:
        raise Exception('Undefined filter [{}] applied.'.format(key))
    return valid_filters[key]

def apply_params_filter(dataframe, params):
    for key, value in params.items():
        filter_generator = get_filter_generator(key)
        dataframe = dataframe[dataframe.apply(filter_generator(value), axis=1)]
    return dataframe
