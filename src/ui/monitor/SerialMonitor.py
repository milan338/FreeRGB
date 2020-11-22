import sys

from Ui_SerialMonitor import Ui_Form  # type: ignore

from PyQt5 import QtWidgets


class SerialMonitor(QtWidgets.QWidget):
    def __init__(self, baudrate=0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def updateMonitor(self, entries=[]):
        print('hi')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = SerialMonitor()
    window.setWindowTitle('FreeRGB Debug View')
    # window.setWindowIcon()
    window.show()

    sys.exit(app.exec())
