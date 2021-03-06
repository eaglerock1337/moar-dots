import filecmp
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
    DEFAULT_PROPERTIES = {
        "create_dirs": False,
        "dotted": False,
        "install": True,
        "replace": False,
    }

    dot_type = "Dot"

    def __init__(self, config):
        self.log = logging.getLogger(__name__)
        self.log.debug(f"Initializing {self.dot_type} object...")

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
                    f"Tried to create a {self.dot_type}, but didn't have a {required} specified!",
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
        self.backup_file = False

    def _get_target_file(self):
        """
        Retrieves target filename
        Goes either by the filename property or the source filename
        """
        try:
            return self.properties["filename"]
        except KeyError:
            return os.path.basename(self.properties["source"])

    def _check_cache(self):
        """
        Check the cache to see if the file was already installed by moar_dots
        Returns True if the cache matches and is installed, otherwise returns False
        """
        self.log.debug(f"Checking cache for {self.name}")

        if self.name in cache:
            self.log.debug(f"There was a cache hit. Checking validity...")

            for key in cache[self.name].keys():
                if key in ["source", "target"]:
                    continue
                if cache[self.name][key] != self.properties[key]:
                    self.log.debug("There was a cache mismatch. Updating file...")
                    return False

            if self.is_installed():
                self.log.info(f"{self.name} is already installed. Skipping...")
                return True
            else:
                self.log.debug(
                    f"{self.name}'s cache is correct but the file appears wrong, installing..."
                )
                return False

        else:
            self.log.debug(f"No cache for {self.name}, installing...")
            return False

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
                f"Please check the config for {self.name} for accuracy.",
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
            self.log.info(
                "Exact filename detected. This will be processed, but this isn't recommended."
            )
            self.log.debug(f"Instead, add 'fieldname' to your {self.dot_type} config.")
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
                self.log.debug(
                    f"Directory {self.target_dir} does not exist. Creating..."
                )
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
                self.log.debug(f"Backing up to {self.target}{BACKUP_EXTENSION}")
                os.rename(self.target, f"{self.target}{BACKUP_EXTENSION}")
                self.backup_file = True
            else:
                Wipe(
                    "FileExistsError",
                    f"The file {self.name} already exists! Please verify the",
                    "target file is correct. If you want this file replaced and backed-up,",
                    "include \"'replace': True\" in the config.",
                )

    def _save_to_cache(self, status):
        """
        Add the file and link information to the moar-dots cachefile
        Updates the status 
        """
        cache[self.name] = {
            "description": self.properties["description"],
            "source": self.source,
            "target": self.target,
            "type": self.dot_type,
            "is_directory": self.properties["is_directory"],
            "status": status,
        }

        if self.backup_file:
            cache["backup"] = f"{self.target}{BACKUP_EXTENSION}"

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

        if self._check_cache():
            self.log.info(f"{self.name} is already installed! Skipping...")
            return

        self._check_source()
        self._set_target()
        self._check_directory()
        self._check_file()

        os.symlink(self.source, self.target)
        self._save_to_cache("installed")

    def is_installed(self):
        """
        Checks the moar_dots cache to see if the symlink was installed.
        """
        if self.name not in cache:
            self.log.debug(f"{self.name} not in cache, so assuming it isn't insalled!")
            return False

        return filecmp.cmp(cache[self.name]["source"], cache[self.name]["target"])

    def nuke_it(self):
        """
        Removes the dotfile symlink and restores original if found
        """
        self.log.info(f"Nuke it: {self.name}")
        self.log.debug("Checking file status...")

        if self.name not in cache:
            self.log.info("File not in cache! Skipping...")
            return

        if cache[self.name]["status"] != "installed":
            self.log.info("File has already been removed. Skipping...")
            return

        if not os.path.islink(cache[self.name]["target"]):
            Wipe(
                "FileNotLinkError",
                f"The file {cache[self.name]['target']} appears to be a link!",
                "The file was most likely moved outside of moar-dots. Please check the file.",
                "You can remove this from the cache by passing '--update-cache' to moar-dots.",
            )

        if not self.is_installed():
            Wipe(
                "FileNotFoundError",
                f"The file {cache[self.name]['target']} is not found!",
                "The might have been removed outside of moar-dots. Please check the file.",
                "You can remove this from cache by passing '--update-cache' to moar-dots.",
            )

        self.log.debug(f"Unlinking {cache[self.name]['target']}...")
        os.unlink(cache["name"]["target"])
        self._save_to_cache("removed")

    def validate_cache(self):
        """
        Processes the Dot in cache to ensure validity.
        Any cache entry not fully validated will be either updated if possible or removed
        """
        self.log.info(f"Updating cache for {self.name}...")
