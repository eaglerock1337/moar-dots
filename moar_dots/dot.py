import logging

from .wipe import Wipe


class Dot:
    """
    The base Dot class used by moar-dots to handle basic dotfiles to be stored
    on the filesystem. Also acts as the parent class for all other file types.
    """

    REQUIRED_ARGS = ['name', 'dotted', 'source', 'target']
    OPTIONAL_ARGS = ['description']
    DEFAULT_ARGS  = {"dotted":False}

    def __init__(self, config):
        self.log = logging.getLogger(__name__)
        self.log.debug("Initializing Dot object...")

        self.properties = {}
        for required in self.REQUIRED_ARGS:
            try:
                self.properties['{required}'] = config.pop(required)
            except KeyError as e:
                Wipe(
                    e,
                    f"Tried to create a dot, but didn't have a {required} specified!",
                    f"Here's the remainder of the config being send to the Dot: {config}",
                )

        for optional in self.OPTIONAL_ARGS:
            try:
                self.properties['{optional}'] = config.pop(optional)
            except KeyError:
                self.log.warn(f"No {optional} specified for {self.properties['name']}.")

        for arg, default in self.DEFAULT_ARGS:
            try:
                self.properties['{arg}'] = config.pop(arg)
            except KeyError:                
                self.log.warn(f"No {arg} specified.for {self.properties['name']}.")
                self.log.warn(f"Defaulting to {default}")
                self.properties['{arg}'] = default

        if config.isEmpty() == False:
            self.log.warn(f"Unexpected parameters found for {self.properties['name']},")
            self.log.warn("Please check your config file for accuracy!")
            self.log.info("Unexpected fields:")
            self.log.info(config)

    def dot_it(self):
        """
        Installs the dotfile via symlink and backs up originals
        """
        pass

    def nuke_it(self):
        """
        Removes the dotfile symlink and restores original if found
        """
        pass
