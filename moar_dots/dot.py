import logging
import os

from .constants import BACKUP_EXTENSION
from .wipe import Wipe


class Dot:
    """
    The base Dot class used by moar-dots to handle basic dotfiles to be stored
    on the filesystem. Also acts as the parent class for all other file types.
    """

    REQUIRED_PROPERTIES = ['name', 'source', 'target']
    OPTIONAL_PROPERTIES = ['description']
    DEFAULT_PROPERTIES  = {"dotted":False, "replace":False, "create_dirs":False}

    def __init__(self, config):
        self.log = logging.getLogger(__name__)
        self.log.debug("Initializing Dot object...")

        self.properties = {}
        for required in self.REQUIRED_PROPERTIES:
            try:
                self.properties['{required}'] = config.pop(required)
            except KeyError as key_error:
                Wipe(
                    key_error,
                    f"Tried to create a dot, but didn't have a {required} specified!",
                    f"Here's the remainder of the config being send to the Dot: {config}",
                )

        for optional in self.OPTIONAL_PROPERTIES:
            try:
                self.properties['{optional}'] = config.pop(optional)
            except KeyError:
                self.log.warn(f"No {optional} specified for {self.properties['name']}.")

        for arg, default in self.DEFAULT_PROPERTIES:
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

    def _check_directory(self):
        """
        Checks if the target's directory exists.
        Will create the directories if specified by 'create_dirs': True.
        """
        target_dir = os.path.dirname(self.properties['target'])
        self.log.debug("Checking for directory {target_dir}...")

        if not os.path.isdir(target_dir):
            if self.properties['create_dirs']:
                self.log.debug(f"Directory {target_dir} does not exist. Creating...")
                os.makedirs(target_dir)
            else:
                Wipe(
                    "NoDirectoryError",
                    f"The directory {target_dir} for {self.properties['name']} does not exist!",
                    "Please verify the target file is correct. If you want moar_dots to",
                    "create the directories for you, include \"'create_dirs': True\" in the config.",
                )

    def _check_file(self):
        """
        Checks if the file exists.
        Will back up and replace existing file if specified by 'replace': True.
        """
        self.log.debug("Checking if the file exists...")
        if os.path.exists(self.properties["target"]):
            if self.properties["replace"]:
                self.log.info(f"File {self.properties['name']} exists. Backing up...")
                self.log.debug(f"Backing up to {self.properties['target']}{BACKUP_EXTENSION}")
                os.rename(self.properties["target"], f"{self.properties['target']}{BACKUP_EXTENSION}")
            else:
                Wipe(
                    "FileExistsError",
                    f"The file {self.properties['name']} already exists! Please verify the",
                    "target file is correct. If you want this file replaced and backed-up,",
                    "include \"'replace': True\" in the config.",
                )
    
    def dot_it(self):
        """
        Installs the dotfile via symlink and backs up originals
        """
        self.log.info(f"DOT it: {self.properties['name']}")

        self.log.debug("Property Dump:")
        dump_properties = dict(self.OPTIONAL_PROPERTIES) + \
                          dict(self.REQUIRED_PROPERTIES) + \
                          dict(self.DEFAULT_PROPERTIES)
        dump_properties.pop("name")

        for property in dump_properties:
            self.log.debug(f"- {property.capitalize()}: {self.properties[property]}")

        self._check_directory()
        self._check_file()

        os.symlink(self.properties["source"], self.properties["target"])
    

    def nuke_it(self):
        """
        Removes the dotfile symlink and restores original if found
        """
        pass
