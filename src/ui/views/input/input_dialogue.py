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

from src import __globals__

from src.ui.generators.create_menu_context import CreateMenuContext
from src.ui.views.input_types import InputTypes
from src.ui.views.input.Ui_input_dialogue import Ui_Form

from src.rw.jsonio import JsonIO

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt


class InputDialogue(QWidget, InputTypes):
    def __init__(self, menu, new_entry=True, btn_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Setup UI
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # Initialise variables
        self.effect_name = None
        self.effect_payload = None
        self.menu = menu
        self.new_entry = new_entry
        self.btn_name = btn_name
        # Get buttons from current menu
        self.page_contents = JsonIO('menus.json').readEntry(self.menu)
        # Initialise effect type selection menu
        self.effectTypeSelect()
        # Open effect drop down when 'effects' button clicked
        self.ui.btn_effect_types.clicked.connect(
            lambda: self.contextMenu(self.menu_effects))
        # Add functionality to 'submit' button
        self.ui.btn_submit.clicked.connect(self.getInputs)
        # Create input types
        super().genValidators(button=self.ui.btn_payload_type,
                              entry=self.ui.input_effect_payload)
        # Get existing data from button if editing
        if new_entry:
            # Clear current menu selection
            __globals__.popup_menu_selection = None
        else:
            # Get button data
            self.btn = JsonIO('menus.json').findElement(self.btn_name)
            # Set existing text entry fields
            self.ui.input_effect_name.setText(self.btn[0])
            self.ui.btn_effect_types.setText(self.btn[1])
            self.ui.input_effect_payload.setText(self.btn[2].split(']')[1])
            self.selected_type = self.btn[2].split(']')[0].split('[')[1]
            self.ui.input_effect_payload.setValidator(
                self.input_types[self.selected_type])
            print(self.selected_type)
            self.ui.btn_payload_type.setText(f'Input: {self.selected_type}')
            # Set current menu selection
            __globals__.popup_menu_selection = self.btn[3]
        # Block inputs to application while dialogue active
        self.setWindowModality(Qt.ApplicationModal)

    def effectTypeSelect(self):
        # Read entries from JSON
        self.effect_types = JsonIO('effects.json').readEntry('effects')
        # Create new right click menu
        self.menu_effects = CreateMenuContext(parent=self).makeMenu()
        # Add all JSON entries as options to right click menu
        for effect_name, effect_class in self.effect_types.items():
            self.menu_args = (self.ui.btn_effect_types, effect_class)
            CreateMenuContext(parent=self).addOption(
                self.menu_effects, effect_name, (self.menu_args))

    def contextMenu(self, menu):
        # Place context menu at cursor position
        menu.exec(QCursor.pos())

    def getInputs(self):
        # Reset user presented error
        self.ui.label_error.setText('')
        # Update variables with user input
        self.effect_name = self.ui.input_effect_name.text()
        self.effect_payload = self.ui.input_effect_payload.text()
        # Ensure no input is blank - falsy when blank
        if not self.effect_name or not self.effect_payload or not __globals__.popup_menu_selection:
            # Raise error to user
            self.ui.label_error.setText('Input(s) cannot be left empty')
        else:
            self.genObjectName(self.effect_name)

    def genObjectName(self, user_input):
        self.object_name = 'btn_effect'
        # Create formatted object name
        for word in user_input.split(' '):
            self.object_name += '_' + word
        self.object_name = self.object_name.lower()
        self.checkInputs(self.object_name)

    def checkInputs(self, generated_object_name):
        # Cycle through existing effects to ensure effect does not exist already
        if self.new_entry:
            for menu in self.page_contents:
                for element in self.page_contents[menu]:
                    if element == generated_object_name:
                        # Raise error to user
                        self.ui.label_error.setText('Effect already exists')
                        return False
            # Only runs if effect does not already exist
            self.createEffect(
                'main_menu', 'main_menu_button_layout', generated_object_name)
            self.exitWindow()
        # Edit existing entry
        else:
            # Replace existing button data with new data
            JsonIO('menus.json').replaceEntry(self.btn_name, generated_object_name,
                                              f'[{self.selected_type}]{self.effect_name}', __globals__.popup_menu_selection, self.effect_payload)
            self.exitWindow()

    def createEffect(self, menu, layout, entry_name):
        self.command = {
            'type': __globals__.popup_menu_selection,
            'payload': f'[{self.selected_type}]{self.effect_payload}'
        }
        JsonIO('menus.json').writeEntry(menu, layout, entry_name,
                                        self.effect_name, self.command, sort_keys=False)

    def exitWindow(self):
        # Update menu layout with new JSON
        __globals__.refreshMenus()
        # Close input menu
        self.close()
