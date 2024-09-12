import argparse
import time
import json
import logging
import signal
import socket
from contextlib import suppress
from datetime import datetime
from http.client import RemoteDisconnected
from queue import Queue
from threading import Thread
from time import sleep
from typing import Any, Dict, Optional, Tuple

from influxdb_client import InfluxDBClient, WriteApi, QueryApi
from influxdb_client.client.write_api import SYNCHRONOUS

def _read_data(query_api: QueryApi, bucket: str, org: str):
    """
    Read data from InfluxDB using a Flux query.
    """
    
    query = f'''
    from(bucket: "{bucket}")
        |> range(start: -1h)
    '''

    tables = query_api.query(query=query, org=org)
    print(tables)
    for table in tables:
        for record in table.records:
            print(f"Time: {record.get_time()}, Value: {record.get_value()}")

def _parse_args() -> Tuple[InfluxDBClient, str, str, bool, int]:
    parser = argparse.ArgumentParser(
        description="Real time receiving and parsing srsRAN Project gnb metrics data and pushing it to influx db."
    )
    parser.add_argument("--port", type=int, required=True, help="Port to listen from.")
    parser.add_argument(
        "--db-config",
        nargs="*",
        required=True,
        help='Data base configuration in the format "key=value key=value"',
    )
    parser.add_argument("--bucket", required=True, help="Bucket to save the data.")
    parser.add_argument(
        "--clean-bucket", action="store_true", help="Remove all data in the bucket before pushing data from input file"
    )
    parser.add_argument("--testbed", required=True, help="Testbed where srsRAN Project was run")
    parser.add_argument(
        "--log-level", default="INFO", help="Server Log level"
    )

    args = parser.parse_args()

    db_config = {key: value for pair_str in args.db_config for key, value in (pair_str.split("=", 1),)}

    return (
        InfluxDBClient(**db_config),
        args.bucket,
        args.testbed,
        args.clean_bucket,
        args.port,
    )


def main():
    """
    Main Entrypoint
    """

    client, bucket, testbed, clean_bucket, port = _parse_args()

    query_api: QueryApi = client.query_api()

    logging.basicConfig(format="%(asctime)s \x1b[32;20m[%(levelname)s]\x1b[0m %(message)s")
    logging.info("Starting srsRAN Project Metrics Server")

    # Reading existing data in the bucket before pushing new data
    while True:
        time.sleep(1)
        _read_data(query_api, bucket, "srs")

if __name__ == "__main__":
    main()
