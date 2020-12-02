import json

from copy import deepcopy

from os import path

from shutil import copyfile


class JsonIO():
    def __init__(self, filename):
        self.base_path = path.dirname(__file__)
        self.preferences_dir = 'preferences'
        self.json_path = path.abspath(
            path.join(self.base_path, '..', '..', self.preferences_dir, filename))
        self.filename_base = filename.split('.')[0] + '_base.json'

        try:
            with open(self.json_path, 'r') as file:
                self.data = json.load(file)
        except:
            pass

    def fileExists(self):
        try:
            if path.isfile(self.json_path):
                return True
            else:
                return False
        except:
            pass

    def copyFromBase(self):
        self.json_path_base = path.abspath(path.join(
            self.base_path, '..', '..', self.preferences_dir, 'base', self.filename_base))
        print(self.json_path_base)
        try:
            copyfile(self.json_path_base, self.json_path)
        except:
            pass

    def clearLayout(self, menu, layout):
        for element in list(self.data[menu][layout].keys()):
            self.data[menu][layout].pop(element, None)
        self.dumpJson()

    def copyLayout(self, menu, layout):
        # Remove entries from layout
        self.clearLayout(menu, layout)
        # Get Base file to copy from
        self.json_path_base = path.abspath(path.join(
            self.base_path, '..', '..', self.preferences_dir, 'base', self.filename_base))
        # Get entries to copy from original file
        self.data_base = None
        try:
            with open(self.json_path_base, 'r') as file:
                self.data_base = json.load(file)
        except:
            pass
        # Copy all elements from base layout
        for element_name, element_contents in self.data_base[menu][layout].items():
            self.data[menu][layout][element_name] = element_contents
        self.dumpJson()

    def dumpJson(self, sort_keys=False):
        try:
            with open(self.json_path, 'w') as file:
                file.write(json.dumps(
                    self.data, indent=4, sort_keys=sort_keys))
                return 1
        except:
            return 0

    def readEntry(self, entry):
        try:
            return self.data[entry]
        except:
            return None

    def writeEntry(self, menu, layout, entry, entry_name, command, sort_keys):
        # Create new json entry
        self.new_json = {
            'text': entry_name,
            'command': command}
        # Add new json entry to existing dictionary
        self.data[menu][layout][entry] = self.new_json
        # Dump new data to file
        self.dumpJson(sort_keys=sort_keys)

    def removeEntry(self, entry):
        # Cycle through menus and layouts in json to find referenced element
        for menu in self.data:
            for layout in self.data[menu]:
                self.data[menu][layout].pop(entry, None)
        # Dump new data to file
        self.dumpJson()

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
#
                # Only run if target element found
                if self.target_name:
                    # Swap element contents
                    self.data[menu][layout].update(
                        {self.target_name: self.element_contents})
                    self.data[menu][layout].update(
                        {self.element_name: self.target_contents})
                    # Swap element names
                    # 1 - Create a deep copy of the original dictionary
                    self.new_dict = deepcopy(self.data)
                    # 2 - Remove all UI elements from target layout in new dictionary
                    for element in list(self.new_dict[menu][layout].keys()):
                        self.new_dict[menu][layout].pop(element, None)
                    # 3 - Add all UI elements back in the same order,
                    #     During this phase, swap the keys of the
                    #     Element to be moved and its target
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
                    self.dumpJson()
