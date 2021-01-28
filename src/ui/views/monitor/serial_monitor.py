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

from datetime import datetime

from src import __globals__
from src import settings

from src.serial.serialio import SerialIO

from src.ui.widgets.toggle_switch import ToggleSwitch
from src.ui.views.input_types import InputTypes
from src.ui.views.monitor.Ui_serial_monitor import Ui_Form

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot


class SerialMonitor(QWidget, InputTypes):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setupUI()
        self.current_text = self.ui.text_display.text()
        # Update screen when serial becomes available
        __globals__.serial.readyRead.connect(self.updateMonitor)

    def setupUI(self):
        self.disableScroll = lambda: self.scrollbar.setValue(
            self.scrollbar.maximum())
        self.scrollbar = self.ui.text_scroll_region.verticalScrollBar()
        self.auto_scroll = True
        # Switch widget
        self.switch = ToggleSwitch()
        self.switch.setChecked(self.auto_scroll)
        self.switch.toggled.connect(lambda: self.toggleScroll())
        self.ui.switch_placeholder.addWidget(self.switch)
        self.toggleScroll()
        # Buttons
        self.ui.btn_serial_clear.clicked.connect(self.clearMonitor)
        self.ui.btn_serial_send.clicked.connect(self.sendSerial)
        # Create input types
        super().genValidators(button=self.ui.btn_input_type,
                              entry=self.ui.input_serial_text)
        # Send input through serial when enter key pressed
        self.ui.input_serial_text.returnPressed.connect(self.sendSerial)
        # Disable autoscroll on scrolling
        self.scrollbar.sliderMoved.connect(
            lambda: self.toggleScroll(state=False))
        self.toggleScroll()

    @pyqtSlot()
    def updateMonitor(self):
        self.curr_time = datetime.now().strftime('%H:%M:%S.%f')[:-4]
        self.current_text = self.ui.text_display.text()
        self.data = SerialIO.read(__globals__.serial)
        self.new_text = f'{self.current_text}\n\n[{self.curr_time}] {self.data}'
        self.ui.text_display.setText(self.new_text)

    def clearMonitor(self):
        self.ui.text_display.setText('')

    def sendSerial(self):
        self.input = self.ui.input_serial_text.text()
        # Send input
        SerialIO.run('write', self.input, out_type=self.selected_type)
        # Clear input field
        self.ui.input_serial_text.setText('')

    def toggleScroll(self, state=None):
        if state is not None:
            if not state:
                self.auto_scroll = state
                self.switch.setChecked(state)
        else:
            self.auto_scroll = self.switch.isChecked()
        # Autoscroll
        if self.auto_scroll:
            self.scrollbar.rangeChanged.connect(self.disableScroll)
        else:
            if self.scrollbar.receivers(self.scrollbar.rangeChanged) > 0:
                self.scrollbar.rangeChanged.disconnect()

    def wheelEvent(self, event):  # TODO only fires when scrolled to top / bottom of scroll region
        self.toggleScroll(state=False)  # PYQT action for scrollbar movement?

    def closeEvent(self, event):
        __globals__.serial.readyRead.disconnect(self.updateMonitor)
