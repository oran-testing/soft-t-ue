import argparse
import json
import logging
import signal
import socket
import time
import os
from typing import Any, Dict, Optional, Tuple
from dotenv import load_dotenv
from datetime import datetime
import threading


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

        self.ue_data = {}

    def read_data(self):
        self.ue_data = {}
        query = f'''
        from(bucket: "{self.bucket}")
            |> range(start: -1h)
        '''
        tables = self.query_api.query(query=query, org=self.org)
        for table in tables:
            table_value = table.records[0].values.get("_field", '')
            start_time = table.records[0].values.get("_start", '')

            for record in table.records:
                rnti = record.values.get('rnti', '')
                if not rnti:
                    continue
                elif rnti not in self.ue_data.keys():
                    self.ue_data[rnti] = {}

                if table_value not in self.ue_data[rnti].keys():
                    self.ue_data[rnti][table_value] = []
                self.ue_data[rnti][table_value].append(((start_time - record.values.get('_time', None)).total_seconds(),record.values.get('_value', 0)))

        return self.ue_data



if __name__ == "__main__":
    test = MetricsClient()
    for key, value in test.read_data().items():
        print(value["bsr"])
