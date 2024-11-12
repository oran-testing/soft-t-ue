#!/usr/bin/python3

import os
import time

import uuid
import argparse
import pathlib
import yaml
import logging
from typing import List, Dict, Union

# Configuration data class
from Config import Config

# UE subprocess manager
from Ue import Ue


logger = logging.getLogger(__name__)


def configure() -> None:
    """
    Reads in CLI arguments
    Parses YAML config
    Configures logging
    """
    script_dir = pathlib.Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Run an srsRAN gNB and Open5GS, then send metrics to the ue_controller")
    parser.add_argument(
        "--config",
        type=pathlib.Path,
        required=True,
        help="Path of YAML config for the controller")
    parser.add_argument("--log-level",
                    default="DEBUG",
                    help="Set the logging level. Options: DEBUG, INFO, WARNING, ERROR, CRITICAL")
    args = parser.parse_args()
    Config.log_level = getattr(logging, args.log_level.upper(), 1)

    if not isinstance(Config.log_level, int):
        raise ValueError(f"Invalid log level: {args.log_level}")

    logging.basicConfig(level=Config.log_level,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

    Config.filename = args.config
    with open(str(args.config), 'r') as file:
        Config.options = yaml.safe_load(file)

def start_processes() -> List[Dict[str, Union[str, Ue, int]]]:
    """
    Starts any necessary processes using Config
    Starts ping and iperf if specified
    """
    process_list: List[Dict[str, Union[str, Ue, int]]] = []

    ue_index = 1

    if Config.options is None:
        raise ValueError("Config.options is None. Please check the configuration.")


    for process_config in Config.options.get("processes", []):
        if process_config["type"] in ["tester", "clean"]:
            if not os.path.exists(process_config["config_file"]):
                raise ValueError(f"Error initializing processes: UE config file not found {process_config['config_file']}")
            new_ue = Ue(ue_index)
            if process_config['type'] == "tester":
                if "args" not in process_config.keys():
                    raise ValueError(f"Error initializing processes: Tester UE requires arguments")
                new_ue.start([process_config["config_file"]] + process_config["args"].split(" "))
            else:
                new_ue.start([process_config["config_file"]])
            process_list.append({
                'id': str(uuid.uuid4()),
                'type': process_config['type'],
                'config': process_config['config_file'],
                'handle': new_ue,
                'index': ue_index
            })
            ue_index += 1
            logger.debug(f"STARTED: {new_ue}")

    return process_list

def await_children() -> None:
    """
    Wait for all child processes to stop
    """
    process_running = True
    while process_running:
        process_running = False
        for process in process_list:
            if process["handle"].isRunning:
                process_running = True
                logger.debug(f"RUNNING: {process['handle']}")
        time.sleep(1)

if __name__ == '__main__':
    configure()

    logging.debug(f"Running as: {os.getlogin()}")

    process_list = start_processes()
    await_children()
