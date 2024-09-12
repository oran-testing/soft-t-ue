#!/bin/bash

source /opt/srsRAN_Project/docker/.env
python3 ./MetricsClient.py --port "${METRICS_SERVER_PORT}" --bucket "${DOCKER_INFLUXDB_INIT_BUCKET}" --testbed default --db-config url="http://localhost:8086" org="${DOCKER_INFLUXDB_INIT_ORG}" token="${DOCKER_INFLUXDB_INIT_ADMIN_TOKEN}"
