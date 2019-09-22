import logging
import sys
"""
logging.py

Simple logging module for moar-dots
"""

log = logging.getLogger(__name__)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logging.Formatter("%(message)s"))
stdout_handler.setLevel(logging.DEBUG)

log.addHandler(stdout_handler)