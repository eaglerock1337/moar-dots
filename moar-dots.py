import argparse
import logging
import os
import sys

from moar_dots import config, Dot, Wipe

"""
moar-dots - More than a Dotfile script!

Requires Python 3.7 to run, because I'm lazy and f-strings are so much prettier.

Usage: TBD

TODOs:
- Everything
"""


class MoarDots:
    """
    A Python utility for managing dotfiles, bash scripts, Python scripts, and custom Python modules
    """

    def __init__(self):
        self._scan_args()
        self._set_logging()

    def _scan_args(self):
        """
        Scans command-line arguments and sets class variables appropriately
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-v", "--verbose", action="store_true", help="Enable verbose output."
        )

        args = parser.parse_args()

        self.verbose = args.verbose

    def _set_logging(self):
        """
        Sets up the logger to print to stdout and sets the verbosity based on the command input.
        """
        log = logging.getLogger()

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(logging.Formatter("%(message)s"))
        stdout_handler.setLevel(logging.DEBUG)

        log.addHandler(stdout_handler)

        log.setLevel(logging.DEBUG)

        self.log = log
