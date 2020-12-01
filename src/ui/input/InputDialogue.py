import sys

from ui.input.Ui_InputDialogue import Ui_Form

from rw.JsonIO import JsonIO

from PyQt5.QtWidgets import QWidget


class InputDialogue(QWidget):
    def __init__(self, input_type, menu, refresh_menus, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.effect_name = None
        self.effect_payload = None

        self.input_type = input_type
        self.menu = menu
        self.refresh_menus = refresh_menus

        self.page_contents = JsonIO('menus.json').readEntry(self.menu)

        self.ui.btn_submit.clicked.connect(self.getInputs)

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
        for menu in self.page_contents:
            for element in self.page_contents[menu]:
                if element == generated_object_name:
                    # Raise error to user
                    self.ui.label_error.setText('Effect already exists')
                    return False
        # Only runs if effect does not already exist
        self.createEffect(
            'main_menu', 'main_menu_button_layout', generated_object_name)

    def createEffect(self, menu, layout, entry_name):
        self.command = {
            'type': self.input_type,
            'payload': self.effect_payload
        }
        JsonIO('menus.json').writeEntry(menu, layout, entry_name,
                                        self.effect_name, self.command, sort_keys=False)
        self.refresh_menus()
