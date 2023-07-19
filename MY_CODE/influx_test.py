import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

#token = os.environ.get("INFLUXDB_TOKEN")
token = "G9dpsaAmx0o6Z6XV6BQaZ9jtHJ--49nptGbys2l7pWiMgcWDhwnKbHYj9XUbQSrJ6bc8sVLYFdqNVgvu8N_16A=="
org = "epu-ntua"
url = "http://enershare.epu.ntua.gr:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

if write_client.ping():
    print("Connection Succesful")


bucket="dummy-data"

write_api = write_client.write_api(write_options=SYNCHRONOUS)
   
for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="epu-ntua", record=point)
  time.sleep(1) # separate points by 1 second



query_api = write_client.query_api()

query = """from(bucket: "dummy-data")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query, org="epu-ntua")

for table in tables:
  for record in table.records:
    print(record)