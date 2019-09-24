import logging
import os

from .config import cache
from .constants import BACKUP_EXTENSION
from .wipe import Wipe


class Dot:
    """
    The base Dot class used by moar-dots to handle basic dotfiles to be stored
    on the filesystem. Also acts as the parent class for all other file types.
    """

    REQUIRED_PROPERTIES = ["name", "source", "target"]
    OPTIONAL_PROPERTIES = ["description", "filename", "is_directory"]
    DEFAULT_PROPERTIES = {"dotted": False, "replace": False, "create_dirs": False}

    def __init__(self, config):
        self.log = logging.getLogger(__name__)
        self.log.debug("Initializing Dot object...")

        self.properties = {}
        for required in self.REQUIRED_PROPERTIES:
            try:
                self.properties[f"{required}"] = config.pop(required)
                self.log.debug(
                    f"{required.capitalize()}: {self.properties['{required}']}"
                )
            except KeyError as key_error:
                Wipe(
                    key_error,
                    f"Tried to create a Dot, but didn't have a {required} specified!",
                    f"Here's the remainder of the config being sent to the Dot: {config}",
                )

        self.name = self.properties["name"]

        for optional in self.OPTIONAL_PROPERTIES:
            try:
                self.properties[f"{optional}"] = config.pop(optional)
                self.log.debug(
                    f"{optional.capitalize()}: {self.properties[{optional}]}"
                )
            except KeyError:
                self.log.warn(f"No {optional} specified for {self.name}.")

        for arg, default in self.DEFAULT_PROPERTIES:
            try:
                self.properties[f"{arg}"] = config.pop(arg)
                self.log.debug(f"{arg.capitalize()}: {self.properties[{arg}]}")
            except KeyError:
                self.log.info(f"No {arg} specified.for {self.name}.")
                self.log.info(f"Defaulting to {default}")
                self.properties[f"{arg}"] = default

        if config.isEmpty() == False:
            self.log.warn(f"Unexpected parameters found for {self.name},")
            self.log.warn("please check your config file for accuracy!")
            self.log.info(f"Unexpected fields: {config}")

        self.target_file = self._get_target_file()

    def _get_target_file(self):
        """
        Retrieves target filename
        Goes either by the filename property or the source filename
        """
        try:
            return self.properties["filename"]
        except KeyError:
            return os.path.basename(self.properties["source"])

    def _check_source(self):
        """
        Validate source file in repo
        Ensures it exists and that it is a file (or a directory if specified)
        """
        self.source = self.properties["source"]
        self.source_file = os.path.basename(self.source)
        self.log.debug(f"Verify source file {self.source_file}...")

        if not os.path.exists(self.source):
            Wipe(
                "SourceNotFoundError",
                f"The source file {self.source} does not exist!",
                f"Please check the config for {self.name} for accuracy."
            )

        self.log.debug(f"Verifying source file type...")
        if self.properties["is_directory"] and not os.path.isdir(self.source):
            Wipe(
                "SourceNotDirectoryError",
                f"The source was supposed to be a directory, but it is a file!",
                f"Please verify the source file and config for {self.name}",
            )
        else:
            self.log.debug(f"Source validated as a directory: {self.source_file}")
            return
        
        if not self.properties["is_directory"] and os.path.isdir(self.source):
            Wipe(
                "SourceNotFIleError",
                f"The source was supposed to be a file, but it is a directory!",
                f"Please verify the source directory and config for {self.name}",
            )
        else:
            self.log.debug(f"Source validated as a file: {self.source_file}")

    def _set_target(self):
        """
        Sets the intended target
        Retrieves filename from either target or source and adds dot if needed
        """
        self.target = self.properties["target"]
        self.log.debug(f"Processing target for {self.name}: {self.target}")

        if self.target.endswith(self.source_file):
            self.log.info("Exact filename detected. This will be processed, but this isn't recommended.")
            self.log.debug("Instead, add 'fieldname' to your Dot config.")
            self.target_dir = os.path.dirname(self.target)
            self.target_file = os.path.basename(self.target)
            return

        if self.properties["dotted"]:
            self.log.debug("File is specified as hidden, so a dot will be added.")
            dot = "."
        else:
            self.log.debug("File is not hidden, so no dot will be added.")
            dot = ""

        self.target_file = dot + self.source_file
        self.target_dir = self.target
        self.target = self.target_dir + self.target_file

    def _check_directory(self):
        """
        Checks if the target's directory exists
        Will create the directories if specified by 'create_dirs': True
        """
        self.log.debug("Checking for target directory...")

        if not os.path.isdir(self.target_dir):
            if self.properties["create_dirs"]:
                self.log.debug(f"Directory {self.target_dir} does not exist. Creating...")
                os.makedirs(self.target_dir, exist_ok=True)
            else:
                Wipe(
                    "NoDirectoryError",
                    f"The directory {self.target_dir} for {self.target_file} does not exist!",
                    f"Please verify the target file for {self.name}. If you want moar_dots to",
                    "create the directories for you, include \"'create_dirs': True\" in the config.",
                )

    def _check_file(self):
        """
        Checks if the target file exists
        Will back up and replace existing file if specified by 'replace': True
        """
        self.log.debug("Checking if the file exists...")
        if os.path.exists(self.target):
            if self.properties["replace"]:
                self.log.info(f"File {self.name} exists. Backing up...")
                self.log.debug(
                    f"Backing up to {self.target}{BACKUP_EXTENSION}"
                )
                os.rename(self.target, f"{self.target}{BACKUP_EXTENSION}")
            else:
                Wipe(
                    "FileExistsError",
                    f"The file {self.name} already exists! Please verify the",
                    "target file is correct. If you want this file replaced and backed-up,",
                    "include \"'replace': True\" in the config.",
                )

    def _check_cache(self):
        """
        Verify the cached link is correctly assigned
        """
        pass

    def _add_to_cache(self):
        """
        Add the file and link information to the moar-dots cachefile
        """
        pass

    def dot_it(self):
        """
        Installs the dotfile via symlink and backs up originals
        """
        self.log.info(f"DOT it: {self.name}")

        self.log.debug("Property Dump:")
        dump_properties = (
            dict(self.OPTIONAL_PROPERTIES)
            + dict(self.REQUIRED_PROPERTIES)
            + dict(self.DEFAULT_PROPERTIES)
        )
        dump_properties.pop("name")

        for property in dump_properties:
            self.log.debug(f"- {property.capitalize()}: {self.properties[property]}")

        self._check_source()
        self._set_target()
        self._check_directory()
        self._check_file()
        self._check_cache()

        os.symlink(self.source, self.target)

        self._add_to_cache()

    def is_installed(self):
        """
        Checks the moar_dots cache to see if the symlink was installed.
        """
        pass

    def nuke_it(self):
        """
        Removes the dotfile symlink and restores original if found
        """
        self.log.info(f"Nuke it: {self.properties['name']}")

        if not os.path.islink(self.properties["target"]):
            self.log.warn("")

        # TODO: Update cache

