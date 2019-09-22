import yaml

from moar_dots import Wipe


class Dot:
    """
    The base Dot class used by moar-dots to handle basic dotfiles to be stored
    on the filesystem. Also acts as the parent class for all other file types.
    """

    def __init__(self, config):
        try:
            self.name = config.pop("name")
        except KeyError as e:
            Wipe(
                e,
                "Tried to create a dot, but didn't have a name specified!",
                f"Here's what was passed in to the class: {config}",
            )

    def dot_it(self):
        pass

    def nuke_it(self):
        pass
