# This file is part of FreeRGB, an app to control lighting devices.
# Copyright (C) 2020 milan338.
#
# FreeRGB is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FreeRGB is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FreeRGB.  If not, see <https://www.gnu.org/licenses/>.

from os import listdir
from os.path import abspath, dirname, join, isfile

from src import Globals

from src.rw.JsonIO import JsonIO


class Effects():
    def __init__(self):
        # Get effects directory
        self.base_path = abspath(dirname(__file__))
        self.effects_path = abspath(join(self.base_path, 'effect'))
        self.effects_files = listdir(self.effects_path)
        # Find valid effects
        self.findEffects()

    def findEffects(self):
        # Store effects dict
        self.effects_dict = {'effects': {}}
        # Find all valid python files
        for file in self.effects_files:
            self.file_path = abspath(join(self.effects_path, file))
            if isfile(self.file_path) and file.endswith('.py') and file != '__init__.py':
                # Format file name
                self.effect = file.split('.py')[0]
                # Import file
                try:
                    self.module = __import__(
                        f'{Globals.effect_import_path}.{self.effect}', fromlist=[None])
                    self.effect_class = getattr(self.module, self.effect)
                    # Get effect name
                    self.effect_name = getattr(
                        self.effect_class, 'effectData')()
                    self.effects_dict['effects'][self.effect_name] = self.effect
                except:
                    pass
        # Write effect data to file
        JsonIO('effects.json').dumpJson(self.effects_dict)
