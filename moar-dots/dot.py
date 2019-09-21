import yaml

class Dot:
    """
    The core Dot class used by moar-dots to handle all different file types.
    """

    def  __init__(self, config):
        self.name = config['name']

    def dot_it(self):
        pass

    def nuke_it(self):
        pass
