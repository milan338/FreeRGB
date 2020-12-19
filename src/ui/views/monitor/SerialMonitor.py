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

from threading import Thread

from time import sleep

from datetime import datetime

from src.ui.widgets.ToggleSwitch import ToggleSwitch
from src.ui.views.monitor.Ui_SerialMonitor import Ui_Form

from PyQt5.QtWidgets import QWidget


class SerialMonitor(QWidget):
    def __init__(self, baudrate=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Qt.AA_CompressHighFrequencyEvents = False
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setupUI()
        self.current_text = self.ui.text_display.text()
        # Start new serial listener thread
        self.thread = Thread(target=self.listener)
        self.thread.start()

    def setupUI(self):
        self.scrollbar = self.ui.text_scroll_region.verticalScrollBar()
        self.auto_scroll = True
        # Switch widget
        self.switch = ToggleSwitch()
        self.switch.setChecked(self.auto_scroll)
        self.switch.toggled.connect(self.toggleScroll)
        self.ui.switch_placeholder.addWidget(self.switch)
        # Buttons
        self.ui.btn_serial_clear.clicked.connect(self.clearSerial)
        self.ui.btn_serial_send.clicked.connect(self.sendSerial)
        # Disable autoscroll on scrolling
        self.scrollbar.sliderMoved.connect(self.disableAutoScroll)

    def sendSerial(self):
        print(self.ui.input_serial_text.text())  # TODO tmp
        # Clear input field
        self.ui.input_serial_text.setText('')

    def clearSerial(self):
        self.ui.text_display.setText('')

    def disableAutoScroll(self):
        self.auto_scroll = False
        self.switch.setChecked(False)

    def toggleScroll(self):
        self.auto_scroll = self.switch.isChecked()

    def listener(self):
        # Wait for window
        sleep(0.5)
        # Loop while debug menu is visible
        while self.isVisible():
            # print(self.scrollbar.slider)
            self.current_text = self.ui.text_display.text()
            self.updateMonitor('line')
            # Autoscroll
            if self.auto_scroll:
                # Scroll to end of view
                self.scrollbar.setValue(self.scrollbar.maximum())
            sleep(0.5)

    def updateMonitor(self, line):
        self.curr_time = datetime.now().strftime('%H:%M:%S.%f')[:-4]
        self.new_text = f'{self.current_text}\n\n[{self.curr_time}] {line}'
        self.ui.text_display.setText(self.new_text)

    def wheelEvent(self, event):  # TODO only fires when scrolled to top / bottom of scroll region
        self.disableAutoScroll()
