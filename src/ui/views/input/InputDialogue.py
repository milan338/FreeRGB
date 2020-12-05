import sys

import Globals

from ui.views.input.Ui_InputDialogue import Ui_Form

from rw.JsonIO import JsonIO

from PyQt5.QtWidgets import QWidget


class InputDialogue(QWidget):
    def __init__(self, input_type, menu, new_entry=True, btn_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.effect_name = None
        self.effect_payload = None

        self.input_type = input_type
        self.menu = menu
        self.new_entry = new_entry
        self.btn_name = btn_name

        self.page_contents = JsonIO('menus.json').readEntry(self.menu)

        self.ui.btn_submit.clicked.connect(self.getInputs)

        if not new_entry:
            # Get button data
            self.btn = JsonIO('menus.json').findElement(self.btn_name)
            # Set existing text entry fields
            self.ui.input_effect_name.setText(self.btn[0])
            self.ui.input_effect_payload.setText(self.btn[1])

    def getInputs(self):
        # Reset user presented error
        self.ui.label_error.setText('')
        # Update variables with user input
        self.effect_name = self.ui.input_effect_name.text()
        self.effect_payload = self.ui.input_effect_payload.text()
        # Ensure no input is blank - falsy when blank
        if not self.effect_name or not self.effect_payload:
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
        # Create new button
        if self.new_entry:
            # Only runs if effect does not already exist
            self.createEffect(
                'main_menu', 'main_menu_button_layout', generated_object_name)
            self.exitWindow()
        # Edit existing entry
        else:
            # Replace existing button data with new data
            JsonIO('menus.json').replaceEntry(self.btn_name,
                                              generated_object_name, self.effect_name, self.effect_payload)
            self.exitWindow()

    def createEffect(self, menu, layout, entry_name):
        self.command = {
            'type': self.input_type,
            'payload': self.effect_payload
        }
        JsonIO('menus.json').writeEntry(menu, layout, entry_name,
                                        self.effect_name, self.command, sort_keys=False)

    def exitWindow(self):
        # Update menu layout with new JSON
        Globals.refreshMenus()
        # Close input menu
        self.close()
