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

# minimum width for serial monitor lines i.e. if the message is too long then instead of shrinking text a horizontal scrollbar will appear - select only appear when need option
import sys

if __name__ == '__main__':
    from Ui_SerialMonitor import Ui_Form  # type: ignore
else:
    from ui.views.monitor.Ui_SerialMonitor import Ui_Form

from PyQt5.QtWidgets import QWidget, QApplication


class SerialMonitor(QWidget):
    def __init__(self, baudrate=0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def updateMonitor(self, entries=[]):
        print('tmp')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = SerialMonitor()
    window.setWindowTitle('ArduRGB Debug View')
    # window.setWindowIcon()
    window.show()

    sys.exit(app.exec())
