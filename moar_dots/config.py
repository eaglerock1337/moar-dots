import logging
import os
import yaml

from .constants import CONFIG_DIR, CONFIG_FILE, EASTER_FILE

"""
config.py

Provides the config file data for moar-dots
"""

try:
    configfile = open(CONFIG_FILE, "r")
    config = yaml.load(configfile, Loader=yaml.FullLoader)
except FileNotFoundError:
    log = logging.getLogger(__name__)
    log.debug("No config file found! Initializing blank config...")
    configfile = ""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    config = {}

try:
    easterfile = open(EASTER_FILE, "r")
    easter = dict(yaml.load(easterfile, Loader=yaml.SafeLoader))
except FileNotFoundError:
    log = logging.getLogger(__name__)
    log.debug("No easter egg file found! Initializing...")
    os.makedirs(CONFIG_DIR, exist_ok=True)
    easter = {"aggro": 0, "dkpminus": 0}
