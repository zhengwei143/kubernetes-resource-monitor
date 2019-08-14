import os
from influxdb import InfluxDBClient

host = os.environ.get('INFLUXDB_HOST')
port = int(os.environ.get('INFLUXDB_PORT'))
user = os.environ.get('INFLUXDB_ADMIN_USERNAME')
password = os.environ.get('INFLUXDB_ADMIN_PASSWORD')
database = os.environ.get('INFLUXDB_DB')

influx_db = InfluxDBClient(host, port, user, password, database)
