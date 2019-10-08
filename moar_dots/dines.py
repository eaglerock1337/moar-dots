import collections
import logging
import yaml

from .config import easter
from .constants import ERROR_FILE

Error = collections.namedtuple("Error", ["Name", "Text", "DKPMinus"])

class Dines:

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.debug("Spawning Dines...")
        print("foo")
        self.errors = []
        error_yaml = self._get_aggro()
        print("poo")
        for my_error in error_yaml:
            print(my_error)
            dkp_minus = 0
            if "dkpminus" in my_error:
                dkp_minus = my_error["dkpminus"]

            self.errors[my_error["aggro"]] = Error(
                                                my_error["error"],
                                                my_error["text"],
                                                dkp_minus
                                             )

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