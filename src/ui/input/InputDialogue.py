import sys

if __name__ == '__main__':
    from Ui_InputDialogue import Ui_Form  # type: ignore
else:
    from ui.input.Ui_InputDialogue import Ui_Form

from rw.JsonIO import JsonIO

from PyQt5 import QtWidgets


class InputDialogue(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.label_error_exists.hide()
        self.ui.label_error_blank.hide()

        self.effect_name = None
        self.effect_payload = None

        self.ui.btn_submit.clicked.connect(self.getInputs)

    def getInputs(self):
        self.ui.label_error_exists.hide()
        self.ui.label_error_blank.hide()

        self.effect_name = self.ui.input_effect_name.text()
        self.effect_payload = self.ui.input_effect_payload.text()
        # Ensure input is not blank
        if not self.effect_name or not self.effect_payload:
            self.ui.label_error_blank.show()
        else:
            self.genObjectName(self.effect_name)

    def genObjectName(self, input):
        self.object_name = 'btn_effect'
        for word in input.split(' '):
            self.object_name += '_' + word
        print(self.object_name)
        self.checkInputs(self.object_name)

    def checkInputs(self, input):
        self.page_contents = JsonIO('menus.json').readEntry('main_menu')
        print(self.page_contents)
        for effect in self.page_contents['main_menu_button_layout'].items():
            print(effect[0])
            if effect[0] == input:
                self.ui.label_error_exists.show()
            else:
                print('clear')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = InputDialogue()
    window.setWindowTitle('Create New Effect')
    # window.setWindowIcon()
    window.show()

    sys.exit(app.exec())
