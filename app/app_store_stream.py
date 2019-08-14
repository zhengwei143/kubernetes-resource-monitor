import os
import asyncio
import urllib3
import datetime as dt
from redis_store import *
from influx_store import *
from utils.helpers import *

streamed_measurement = "streamed_data"

def get_most_recent_resource_version(resource):
    result_set = influx_db.query("SELECT MAX(resource_version), resource FROM {} WHERE resource=\'{}\'"
        .format(streamed_measurement, resource))
    print(list(result_set.get_points()))
    points = list(map(lambda x: x['max'], result_set.get_points()))
    if not points:
        return None
    return points[0]


def serialize_dataframe_row(row, resource):
    time = None
    if row['event_streamed'] == Event.added:
        time = row['object_streamed']['metadata'].get('creationTimestamp')
    elif row['event_streamed'] == Event.deleted:
        time = row['object_streamed']['metadata'].get('deletionTimestamp')
    if not time:
        return None

    time_occurred = convert_to_current_timezone(parse_datetime_str(time))
    delay_seconds = (row["time_streamed"] - time_occurred).total_seconds()
    return {
        "measurement": "streamed_data",
        "tags": {
            "resource": resource,
            "event": row["event_streamed"]
        },
        "time": time_occurred,
        "fields": {
            "delay": delay_seconds,
            "resource_version": row["resource_version_streamed"]
        }
    }


api_resources = ['deployment', 'pod', 'service', 'pvc', 'ingress', 'node']
def store_streamed_data():
    dataframes = {}
    for resource in api_resources:
        stream_key = get_key(resource, 'streamed')
        df = retrieve_dataframe(stream_key)
        # Take only stable streamed events that are either ADDED or DELETED
        dataframes[resource] = df[
            (df['stable_streamed']) &
            ((df['event_streamed'] == Event.added) |
            (df['event_streamed'] == Event.deleted))]

    influx_rows = []
    for resource, df in dataframes.items():
        # Retrieve the latest resource_version of the resource from influxdb
        recent_rv = get_most_recent_resource_version(resource)
        # Filter the existing streamed dataframe so that we do not serialize/insert duplicate rows
        if recent_rv:
            df = df[df['resource_version_streamed'] > recent_rv]

        for _, row in df.iterrows():
            if row['event_streamed'] == Event.modified:
                continue
            serialized_influx_row = serialize_dataframe_row(row, resource)
            if not serialized_influx_row:
                continue
            influx_rows.append(serialized_influx_row)

    influx_db.write_points(influx_rows)

async def schedule_store_stream():
    while True:
        store_streamed_data()
        await asyncio.sleep(300)

if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    database = os.environ.get('INFLUXDB_DB')
    existing_databases = list(map(lambda x: x['name'], influx_db.get_list_database()))
    if database not in existing_databases:
        influx_db.create_database(database)

    res = influx_db.query('SELECT "delay" FROM "streamed_data"')
    points = list(map(lambda x: x['delay'], res.get_points()))
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(schedule_store_stream())
    except Exception as error:
        print("Error in async loop: {}".format(error))
    finally:
        loop.close()
