import logging
import yaml

from .constants import CONFIG_FILE
"""
config.py

Provides the config file data for moar-dots
"""

try:
    configfile = open(CONFIG_FILE, "r")
except FileNotFoundError:
    log = logging.getLogger(__name__)
    log.debug("No config file found! Initializing blank config...")
    configfile = ""

config = yaml.load(configfile, Loader=yaml.FullLoader) or {}
