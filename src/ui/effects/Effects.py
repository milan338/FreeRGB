import sys

from os import listdir, path

from rw.JsonIO import JsonIO


class Effects():
    def __init__(self):
        # Get effects directory
        self.base_path = path.dirname(__file__)
        self.effects_path = path.abspath(path.join(self.base_path, 'effect'))
        self.effects_files = listdir(self.effects_path)
        self.import_path = 'ui.effects.effect'
        # Find valid effects
        self.findEffects()

    def findEffects(self):
        # Store effects dict
        self.effects_dict = {'effects': {}}
        # Find all valid python files
        for file in self.effects_files:
            self.file_path = path.abspath(path.join(self.effects_path, file))
            if path.isfile(self.file_path) and file.endswith('.py') and file != '__init__.py':
                # Format file name
                self.effect = file.split('.py')[0]
                # Import file
                try:
                    self.module = __import__(
                        f'{self.import_path}.{self.effect}', fromlist=[None])
                    self.effect_class = getattr(self.module, self.effect)
                    # Get effect name
                    self.effect_name = getattr(
                        self.effect_class, 'effectData')()
                    self.effects_dict['effects'][self.effect_name] = self.effect
                except:
                    pass
        print(self.effects_dict)
        # Write effect data to file
        JsonIO('effects.json').dumpJson(self.effects_dict)
