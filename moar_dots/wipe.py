import logging
import os
import random
import yaml

from time import sleep

from .config import easter
from .constants import EASTER_FILE, ERROR_FILE


class Wipe:
    """
    An very strongly themed error handling class for moar-dots.
    Also has an easter egg.
    """

    def __init__(self, error, *args):
        self.log = logging.getLogger(__name__)
        self.log.debug("Initializing Wipe object...")

        self.error = error
        self.text = []
        for arg in args:
            self.text.append(arg)

        self.errors = self._get_aggro()
        self._onyxia_wipe()

    def _get_aggro(self):
        """
        Retrieve all error messages from the error YAML file.
        """
        self.log.debug("Retrieving all error messages...")
        errors = []

        with open(ERROR_FILE, "r") as file:
            errors = list(yaml.load_all(file, Loader=yaml.FullLoader))

        return errors

    def _roll_for_error(self, aggro):
        """
        Returns a random error based on the aggro level passed in.
        """
        self.log.debug("Rolling for an error under aggro level %d...", aggro)
        error_choices = []

        for error in self.errors:
            if error["aggro"] <= aggro:
                error_choices.append(error)
            else:
                break

        self.log.debug(f"Retrieved {len(error_choices)} error(s), choosing one...")
        random.seed()
        return random.choice(error_choices)

    def _onyxia_wipe(self):
        """
        Handles error reporting for issues with moar-dots.
        Also prints out funny output and manages the easter egg.
        """
        self.log.debug("Starting Onyxia Wipe...")

        error = self._roll_for_error(easter["aggro"])
        self.log.debug(f"Error retrieved: {error['error']}")
        self.log.info("=" * 70)
        for line in error["text"]:
            self.log.info(line)
            sleep(2)

        self.log.info("=" * 70)
        self.log.error("(Seriously though, moar-dots had a sad.)")
        self.log.error(f"\nException: {self.error}")
        self.log.error("\nHere's some info about what happened:")
        for line in self.text:
            print(f"  {line}")

        self.log.debug("Updating easter egg data and quitting...")
        easter["aggro"] += 1
        if "dkpminus" in error:
            easter["dkpminus"] += error["dkpminus"]
            self.log.error(
                f"\nOh, and by the way, that was a {error['dkpminus']} DKP minus."
            )

        with open(EASTER_FILE, "w+") as file:
            file.write(yaml.dump(easter))
