import logging
import random
import yaml

from .config import config
from .constants import CONFIG_FILE, ERROR_FILE

class Wipe:
    """
    An very strongly themed error handling class for moar-dots
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
            errors = yaml.load_all(file)
            self.log.debug("Here's what we got: {errors}")
        
        return errors

    def _roll_for_error(self, aggro):
        """
        Returns a random error based on the aggro level passed in.
        """
        self.log.debug(f"Rolling for an error under aggro level {aggro}...")
        error_choices = []

        for error in self.errors:
            if error['aggro'] <= aggro:
                error_choices.append(error)
            else:
                break

        self.log.debug(f"Retrieved {len(error_choices)} errors, choosing one...")
        return random.choice(error_choices)

    def _onyxia_wipe(self):
        """
        Handles error reporting for issues with moar-dots.
        Also prints out funny output and manages the easter egg.
        """
        self.log.debug("Starting Onyxia Wipe...")

        self.log.warn("Temporary config hack in place...remove me eventually!")
        # TODO: Remove this once the config import is complete!
        if not "aggro" in config:
            config["aggro"] = 0
        if not "dkpminus" in config:
            config["dkpminus"] = 0

        error = self._roll_for_error(config["aggro"])
        # log.debug(f"Error retrieved: {error["error"]}")
        self.log.info("=" * 60)
