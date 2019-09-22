import os

"""
constants.py

Global constant variables for moar-dots
"""

CONFIG_DIR = os.path.join(os.getenv("HOME"), ".config/moar-dots")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.yml")
EASTER_FILE = os.path.join(CONFIG_DIR, ".easter.yml")
ERROR_FILE = "moar_dots/data/error.yml"