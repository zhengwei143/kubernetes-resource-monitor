def print_dataframe(df, name=''):
    if 'resource_version' in df.columns:
        sorted_df = df.sort_values(by=['namespace', 'pod_name', 'resource_version'])
    elif 'resource_version_x' in df.columns:
        sorted_df = df.sort_values(by=['namespace', 'pod_name', 'resource_version_x', 'resource_version_y'])
    else:
        sorted_df = df.sort_values(by=['namespace', 'pod_name'])

    sorted_df = sorted_df.reset_index(drop=True)
    print('\n========================================== Dataframe: {} =========================================='.format(name))
    print(sorted_df)

def check_to_add_entry(existing_resource_version, new_resource_version):
    if existing_resource_version is None:
        return True
    if new_resource_version is None:
        return False
    return existing_resource_version < new_resource_version
