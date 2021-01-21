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

import json

from src import settings
from src import __globals__

from copy import deepcopy

from os.path import abspath, dirname, join, isfile

from shutil import copyfile


class JsonIO():
    def __init__(self, filename):
        self.filename = filename
        self.base_path = abspath(dirname(__file__))
        self.preferences_dir = 'preferences'
        self.json_path = abspath(
            join(self.base_path, '..', '..', self.preferences_dir, filename))
        self.filename_base = filename.split('.')[0] + '_base.json'
        try:
            with open(self.json_path, 'r') as file:
                self.data = json.load(file)
        except:
            if settings.do_logs:
                __globals__.logger.error(
                    f'Failed to open JSON file {self.filename} for reading')

    def dumpJson(self, data, sort_keys=False):
        try:
            with open(self.json_path, 'w') as file:
                file.write(json.dumps(data, indent=4, sort_keys=sort_keys))
        except:
            if settings.do_logs:
                __globals__.logger.error(
                    f'Failed to write to JSON file {self.filename}')

    def fileExists(self):
        return isfile(self.json_path)

    def getEffectType(self, effect):
        # Get name of effect
        # print(effect)
        self.effects_path = abspath(
            join(self.base_path, '..', '..', self.preferences_dir, 'effects.json'))
        try:
            # Open effects file
            with open(self.effects_path, 'r') as file:
                self.effects_data = json.load(file)
                for effect_name, effect_data in self.effects_data['effects'].items():
                    if effect_data == effect:
                        return effect_name
                return None
        except:
            if settings.do_logs:
                __globals__.logger.error(
                    f'Failed to open JSON file effects.json for reading')

    def findElement(self, element):
        for menu in self.data.values():
            for layout in menu.values():
                for element_name, element_contents in layout.items():
                    if element_name == element:
                        self.effect_name = self.getEffectType(
                            element_contents['command']['type'])
                        # Return element data
                        return(element_contents['text'], self.effect_name, element_contents['command']['payload'], element_contents['command']['type'])
        return None

    def copyFromBase(self):
        self.json_path_base = abspath(join(
            self.base_path, '..', '..', self.preferences_dir, 'base', self.filename_base))
        try:
            copyfile(self.json_path_base, self.json_path)
        except:
            if settings.do_logs:
                __globals__.logger.error(
                    f'Failed to copy file {self.filename_base} to {self.filename}')

    def clearLayout(self, menu, layout):
        for element in list(self.data[menu][layout].keys()):
            self.data[menu][layout].pop(element, None)
        self.dumpJson(self.data)

    def copyLayout(self, menu, layout):
        # Remove entries from layout
        self.clearLayout(menu, layout)
        # Get Base file to copy from
        self.json_path_base = abspath(join(
            self.base_path, '..', '..', self.preferences_dir, 'base', self.filename_base))
        # Get entries to copy from original file
        self.data_base = None
        try:
            with open(self.json_path_base, 'r') as file:
                self.data_base = json.load(file)
        except:
            if settings.do_logs:
                __globals__.logger.error(
                    f'Failed to open JSON file {self.filename_base} for reading')
        # Copy all elements from base layout
        for element_name, element_contents in self.data_base[menu][layout].items():
            self.data[menu][layout][element_name] = element_contents
        self.dumpJson(self.data)

    def readEntry(self, entry):
        try:
            return self.data[entry]
        except:
            if settings.do_logs:
                __globals__.logger.error(
                    f'Failed to read entry {entry} from JSON file {self.filename}')

    def writeEntry(self, menu, layout, entry, entry_name, command, sort_keys):
        # Create new json entry
        self.new_json = {
            'text': entry_name,
            'command': command}
        # Add new json entry to existing dictionary
        self.data[menu][layout][entry] = self.new_json
        # Dump new data to file
        self.dumpJson(self.data, sort_keys=sort_keys)

    def writeRaw(self, menu, layout, entry_name, entry_contents, sort_keys):
        # Add new json entry to existing dictionary
        self.data[menu][layout][entry_name] = entry_contents
        # Dump new data to file
        self.dumpJson(self.data, sort_keys=sort_keys)

    def copyEntry(self, from_entry, to_entry, to_menu, to_layout, sort_keys):
        # Find entry to copy
        self.from_data = self.findElement(from_entry)
        self.from_name = list(self.from_data.keys())[0]
        print(self.from_name)
        # Write entry to new location
        # self.writeEntry(to_menu, to_layout, )

    def removeEntry(self, entry):
        # Cycle through menus and layouts in json to find referenced element
        for menu in self.data:
            for layout in self.data[menu]:
                self.data[menu][layout].pop(entry, None)
        # Dump new data to file
        self.dumpJson(self.data)

    def removeSingleEntry(self, menu, entry):
        # Cycle through layouts in json menu to find referenced element
        for layout in self.data[menu]:
            self.data[menu][layout].pop(entry, None)
        # Dump new data to file
        self.dumpJson(self.data)

    def shiftEntry(self, entry, direction):
        # Buffers for original element
        self.element_name = None
        self.element_contents = None
        # Buffers for target element
        self.target_name = None
        self.target_contents = None
        self.target_position = None
        # Cycle through menus and layouts in json to find referenced element
        for menu in self.data:
            for layout in self.data[menu]:
                self.n = 0
                for element_name, element_contents in self.data[menu][layout].items():
                    # When element is found
                    if element_name == entry.objectName():
                        # Store original element
                        self.element_name = element_name
                        self.element_contents = element_contents
                        # Get element positions
                        self.target_position = self.n + direction
                        break
                    else:
                        self.n += 1

                # Only run if original element found
                if self.element_name:
                    # Get data from target element
                    self.n = 0
                    for element_name, element_contents in self.data[menu][layout].items():
                        if self.n == self.target_position:
                            # Store target element
                            self.target_name = element_name
                            self.target_contents = element_contents
                            break
                        else:
                            self.n += 1

                # Only run if target element found
                if self.target_name:
                    # Swap element contents
                    self.data[menu][layout].update(
                        {self.target_name: self.element_contents})
                    self.data[menu][layout].update(
                        {self.element_name: self.target_contents})
                    # Create blank copy of main data
                    self.blankCopy(menu, layout)
                    # Add all UI elements back to blank copy in the same order,
                    # During this phase, swap the keys of the Element to be moved and its target
                    for element_name, element_contents in self.data[menu][layout].items():
                        # Change original element to target element
                        if element_name == self.element_name:
                            self.new_dict[menu][layout][self.target_name] = element_contents
                        # Change target element to original element
                        elif element_name == self.target_name:
                            self.new_dict[menu][layout][self.element_name] = element_contents
                        # Keep element the same
                        else:
                            self.new_dict[menu][layout][element_name] = element_contents
                    # Dump new data to file
                    self.data = self.new_dict
                    self.dumpJson(self.data)

    def replaceEntry(self, old_element, new_element, new_element_name, new_element_type, new_element_contents):
        # Go through JSON to find element
        for menu_name, menu_contents in self.data.items():
            for layout_name, layout_contents in menu_contents.items():
                for element in layout_contents.keys():
                    if element == old_element:
                        # Create blank copy of main data
                        self.blankCopy(menu_name, layout_name)
                        # Element contents
                        self.new_element_contents = {'text': new_element_name,
                                                     'command': {
                                                         'type': new_element_type,
                                                         'payload': new_element_contents}}
                        # Add original UI elements back to blank copy
                        # Replace original element with new name
                        for element_name, element_contents in layout_contents.items():
                            # Add modified element
                            if element_name == old_element:
                                self.new_dict[menu_name][layout_name][new_element] = self.new_element_contents
                            # Add original element
                            else:
                                self.new_dict[menu_name][layout_name][element_name] = element_contents
                        # Dump new data to file
                        self.data = self.new_dict
                        self.dumpJson(self.data)

    def blankCopy(self, menu, layout):
        # Create a deep copy of the original dictionary
        self.new_dict = deepcopy(self.data)
        # Remove all UI elements from target layout in new dictionary
        for element in list(self.new_dict[menu][layout].keys()):
            self.new_dict[menu][layout].pop(element, None)
