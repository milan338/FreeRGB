# minimum width for serial monitor lines i.e. if the message is too long then instead of shrinking text a horizontal scrollbar will appear - select only appear when need option
import sys
import os

from ui.monitor.Ui_SerialMonitor import Ui_Form

from PyQt5 import QtWidgets


class SerialMonitor(QtWidgets.QWidget):
    def __init__(self, baudrate=0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        print(os.getcwd())

    def updateMonitor(self, entries=[]):
        print('tmp')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = SerialMonitor()
    window.setWindowTitle('FreeRGB Debug View')
    # window.setWindowIcon()
    window.show()

    sys.exit(app.exec())
