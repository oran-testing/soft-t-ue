import argparse
import os
# Disable kivy arguments
os.environ["KIVY_NO_ARGS"] = "1"
import pathlib
import yaml
import logging

# Main GUI application
from MainApp import MainApp
# Configuration data class
from Config import Config


def configure():
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
    Config.log_level = getattr(logging, args.log_level.upper(), None)

    if not isinstance(Config.log_level, int):
        raise ValueError(f"Invalid log level: {args.log_level}")

    logging.basicConfig(level=Config.log_level,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

    Config.filename = args.config
    with open(str(args.config), 'r') as file:
        Config.options = yaml.safe_load(file)

if __name__ == '__main__':
    configure()
    logging.debug("Killing old processes...")
    os.system("kill -9 $(ps aux | awk '/srsue/ && !/main/{print $2}') > /dev/null 2>&1")

    logging.debug(f"Running as: {os.getlogin()}")

    MainApp().run()
