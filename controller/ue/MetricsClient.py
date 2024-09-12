import argparse
import json
import logging
import signal
import socket
import time
import os
from typing import Any, Dict, Optional, Tuple
from dotenv import load_dotenv


from influxdb_client import InfluxDBClient, QueryApi
from influxdb_client.client.write_api import SYNCHRONOUS


class MetricsClient:

    def __init__(self):
        load_dotenv("/opt/srsRAN_Project/docker/.env")
        self.bucket = os.environ.get("DOCKER_INFLUXDB_INIT_BUCKET")
        self.org = os.environ.get("DOCKER_INFLUXDB_INIT_ORG")
        self.token = os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")
        self.query_api: QueryApi = InfluxDBClient(
            **{
                "url": "http://localhost:8086",
                "org": self.org,
                "token": self.token
            }
        ).query_api()

    def read_data(self):
        query = f'''
        from(bucket: "{self.bucket}")
            |> range(start: -1h)
        '''
        tables = self.query_api.query(query=query, org=self.org)
        print(tables)
        for table in tables:
            for record in table.records:
                print(f"Time: {record.get_time()}, Value: {record.get_value()}")
        return tables



if __name__ == "__main__":
    test = MetricsClient()
    while True:
        time.sleep(1)
        test = test.read_data()
