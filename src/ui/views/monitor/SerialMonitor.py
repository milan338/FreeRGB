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

from ui.views.monitor.Ui_SerialMonitor import Ui_Form

from threading import Thread

from time import sleep

from datetime import datetime

from PyQt5.QtWidgets import QWidget


class SerialMonitor(QWidget):
    def __init__(self, baudrate=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.current_text = self.ui.text_display.text()
        # Start new serial listener thread
        self.thread = Thread(target=self.listener)
        self.thread.start()

    def listener(self):
        # Wait for window
        sleep(0.5)
        # Loop while debug menu is visible
        while self.isVisible():
            self.current_text = self.ui.text_display.text()
            self.updateMonitor('line')
            # Autoscroll TODO autoscroll toggle, untoggles when user moves scrollbar
            self.ui.text_scroll_region.verticalScrollBar().setValue(
                self.ui.text_scroll_region.verticalScrollBar().maximum())
            sleep(0.5)

    def updateMonitor(self, line):
        self.curr_time = datetime.now().strftime('%H:%M:%S.%f')[:-4]
        self.new_text = f'{self.current_text}\n\n[{self.curr_time}] {line}'
        self.ui.text_display.setText(self.new_text)
