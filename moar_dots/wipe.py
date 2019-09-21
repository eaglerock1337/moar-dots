import yaml
import logging

class Wipe:
    """
    An very themed error handling class for moar-dots
    """

    error_file = "data/error.yml"

    def __init__(self, error, *args):
        self.error = error
        self.text = []
        for arg in args:
            self.text.append(arg)

        self.errors = self._get_aggro()
        self.log = logging.getLogger(__name__)
        self._onyxia_wipe()

    def _get_aggro(self):
        """
        Retrieve all error messages from the error YAML file.
        """
        with open(self.error_file, "r") as file:
            errors = yaml.load_all(file)
        return errors

    def _get_error(self):
        pass

    def _onyxia_wipe(self):
        pass

