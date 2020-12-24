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

from src import Globals

from src.serial.SerialIO import SerialIO

from src.ui.widgets.ToggleSwitch import ToggleSwitch
from src.ui.views.monitor.Ui_SerialMonitor import Ui_Form
from src.ui.generators.CreateMenuContext import CreateMenuContext

from PyQt5.QtGui import QCursor, QRegExpValidator
from PyQt5.QtWidgets import QWidget, QAction
from PyQt5.QtCore import pyqtSlot, QRegExp


class SerialMonitor(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setupUI()
        self.current_text = self.ui.text_display.text()
        # Update screen when serial becomes available
        Globals.serial.readyRead.connect(self.updateMonitor)

    def setupUI(self):
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
        # Input
        self.input_menu = CreateMenuContext(parent=self).makeMenu()
        self.input_menu.triggered.connect(self.updateInputType)
        # Regex validator instead of int validator allows for commas to be captured
        self.int_filter = QRegExp('[\d*\,]*')
        self.int_validator = QRegExpValidator(self.int_filter)
        self.input_types = {'Integer': self.int_validator, 'String': None}
        self.ui.btn_input_type.clicked.connect(self.initTypeMenu)
        self.selected_type = 'Integer'
        self.ui.btn_input_type.setText('Input: Integer')
        self.ui.input_serial_text.setValidator(self.int_validator)
        self.ui.input_serial_text.returnPressed.connect(self.sendSerial)
        # Disable autoscroll on scrolling
        self.scrollbar.sliderMoved.connect(
            lambda: self.toggleScroll(state=False))

    def initTypeMenu(self):
        self.input_menu.clear()
        for input_type, validator_type in self.input_types.items():
            if input_type == self.selected_type:
                CreateMenuContext(parent=self).addOption(
                    self.input_menu, input_type, (self.ui.btn_input_type, validator_type), highlighted=True)
            else:
                CreateMenuContext(parent=self).addOption(
                    self.input_menu, input_type, (self.ui.btn_input_type, validator_type))
        self.input_menu.exec(QCursor.pos())

    @pyqtSlot(QAction)
    def updateInputType(self, action):
        self.selected_type = action.text()
        self.ui.btn_input_type.setText(f'Input: {self.selected_type}')
        self.ui.input_serial_text.setValidator(Globals.popup_menu_selection)
        self.ui.input_serial_text.clear()

    def sendSerial(self):
        self.input = self.ui.input_serial_text.text()
        # Send integer input
        if self.selected_type == 'Integer':
            try:
                # Split input for multiple args
                self.input_array = self.input.split(',')
                self.input_array = [int(item) for item in self.input_array]
                self.input_array = bytearray(self.input_array)
                SerialIO.run(Globals.serial, 'write', self.input_array)
            except:
                Globals.logger.warn(
                    f'Failed to convert input {self.input} to bytearray')
        # Send string input
        else:
            SerialIO.run(Globals.serial, 'write', self.input.encode())
        # Clear input field
        self.ui.input_serial_text.setText('')

    @pyqtSlot()
    def updateMonitor(self):
        self.curr_time = datetime.now().strftime('%H:%M:%S.%f')[:-4]
        self.current_text = self.ui.text_display.text()
        self.data = SerialIO.read(Globals.serial)
        self.new_text = f'{self.current_text}\n\n[{self.curr_time}] {self.data}'
        self.ui.text_display.setText(self.new_text)

    def clearMonitor(self):
        self.ui.text_display.setText('')

    def toggleScroll(self, state=None):
        if state is not None:
            if not state:
                self.auto_scroll = state
                self.switch.setChecked(state)
        else:
            self.auto_scroll = self.switch.isChecked()
        # Autoscroll
        if self.auto_scroll:
            self.scrollbar.rangeChanged.connect(
                lambda: self.scrollbar.setValue(self.scrollbar.maximum()))
        else:
            self.scrollbar.disconnect()
            self.scrollbar.sliderMoved.connect(
                lambda: self.toggleScroll(state=False))

    def wheelEvent(self, event):  # TODO only fires when scrolled to top / bottom of scroll region
        self.toggleScroll(state=False)
