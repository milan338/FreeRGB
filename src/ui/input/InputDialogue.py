import sys

from ui.input.Ui_InputDialogue import Ui_Form

from rw.JsonIO import JsonIO

from PyQt5 import QtWidgets


class InputDialogue(QtWidgets.QWidget):
    def __init__(self, input_type, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.effect_name = None
        self.effect_payload = None

        self.input_type = input_type

        self.ui.btn_submit.clicked.connect(self.getInputs)

    def getInputs(self):
        self.ui.label_error.setText('')

        self.effect_name = self.ui.input_effect_name.text()
        self.effect_payload = self.ui.input_effect_payload.text()
        # Ensure input is not blank
        if not self.effect_name or not self.effect_payload:
            self.ui.label_error.setText('Input(s) cannot be left empty')
        else:
            self.genObjectName(self.effect_name)

    def genObjectName(self, user_input):
        self.object_name = 'btn_effect'
        for word in user_input.split(' '):
            self.object_name += '_' + word
        self.object_name = self.object_name.lower()
        self.checkInputs(self.object_name)

    def checkInputs(self, generated_object_name):
        self.page_contents = JsonIO('menus.json').readEntry('main_menu')
        for effect in self.page_contents['main_menu_button_layout'].items():
            # Check if effect in JSON file matches user input
            if effect[0] == generated_object_name:
                self.ui.label_error.setText('Effect already exists')
                return False
        self.createEffect(
            'main_menu', 'main_menu_button_layout', generated_object_name)

    def createEffect(self, menu, layout, entry_name):
        self.command = {
            'type': self.input_type,
            'payload': self.effect_payload
        }
        JsonIO('menus.json').writeEntry(menu, layout,
                                        entry_name, self.effect_name, self.command)
