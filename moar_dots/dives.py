import collections
import logging
import yaml

from .config import easter
from .constants import ERROR_FILE

ErrorQuote = collections.namedtuple("ErrorQuote", "Name, Text, Aggro, DKPMinus")

class Dives:
    """
    A Class for containing and interacting with all Dives error quotes.
    Quotes are defined as a list of named tuples that make referencing the object easy.
    """
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.debug("Spawning Dives...")
        self.errors = self._unpack_quotes()

    def __len__(self):
        return len(self.errors)

    def __getitem__(self, position):
        return self.errors[position]

    def _get_aggro(self):
        """
        Retrieve all error messages from the error YAML file.
        """
        self.log.debug("Retrieving all error messages...")
        errors = []

        with open(ERROR_FILE, "r") as file:
            errors = list(yaml.load_all(file, Loader=yaml.FullLoader))

        return errors

    def _unpack_quotes(self):
        quotes = []
        error_yaml = self._get_aggro()
        for my_error in error_yaml:
            dkp_minus = 0
            if "dkpminus" in my_error.keys():
                dkp_minus = my_error["dkpminus"]

            my_error_tuple = ErrorQuote(my_error["error"], my_error["text"], my_error["aggro"], dkp_minus)
            quotes.append(my_error_tuple)

        return quotes