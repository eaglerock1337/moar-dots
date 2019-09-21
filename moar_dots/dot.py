import yaml

from moar_dots import Wipe

class Dot:
    """
    The core Dot class used by moar-dots to handle all different file types.
    """

    def __init__(self, config):
        try:
            self.name = config.pop('name')
        except KeyError as e:
            Wipe(
                e,
                "Tried to create a Dot, but didn't have a name specified!",
                f"Here's what was passed in to the class: {config}"
            )

    def dot_it(self):
        pass

    def nuke_it(self):
        pass
