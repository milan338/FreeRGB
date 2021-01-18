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
from src.ui.views.monitor.Ui_serial_monitor import Ui_Form
from src.ui.generators.create_menu_context import CreateMenuContext

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
        # Input
        self.input_menu = CreateMenuContext(parent=self).makeMenu()
        self.input_menu.triggered.connect(self.updateInputType)
        # Integer-only message
        self.int_filter = QRegExp('[\d*\,]*')
        self.int_validator = QRegExpValidator(self.int_filter)
        # Integer-char message
        self.int_char_filter = QRegExp('[\d*a-z\,]*')
        self.int_char_validator = QRegExpValidator(self.int_char_filter)
        # Set up filters
        self.input_types = {'Integer': self.int_validator,
                            'Integer-Char': self.int_char_validator,
                            'String': None}
        self.ui.btn_input_type.clicked.connect(self.initTypeMenu)
        self.selected_type = 'Integer'
        self.ui.btn_input_type.setText('Input: Integer')
        self.ui.input_serial_text.setValidator(self.int_validator)
        self.ui.input_serial_text.returnPressed.connect(self.sendSerial)
        # Disable autoscroll on scrolling
        self.scrollbar.sliderMoved.connect(
            lambda: self.toggleScroll(state=False))
        self.toggleScroll()

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
        self.ui.input_serial_text.setValidator(
            __globals__.popup_menu_selection)
        self.ui.input_serial_text.clear()

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
        # Send integer input
        if self.selected_type == 'Integer':
            try:
                # Split input for multiple args
                self.input_array = self.input.split(',')
                self.input_array = [int(item) for item in self.input_array]
                self.input_array = bytearray(self.input_array)
                SerialIO.run(__globals__.serial, 'write', self.input_array)
            except:
                if settings.do_logs:
                    __globals__.logger.warn(
                        f'Failed to convert input {self.input} to bytearray')
        elif self.selected_type == 'Integer-Char':
            try:
                # Split string and integer parts
                self.input_array = self.input.split(',')
                self.output_bytes = b''
                for entry in self.input_array:
                    if entry:
                        try:
                            entry = int(entry).to_bytes(1, byteorder='big')
                        except ValueError:
                            entry = entry.encode()
                        self.output_bytes += entry
                print(bytearray(self.output_bytes))
                SerialIO.run(__globals__.serial, 'write',
                             bytearray(self.output_bytes))
            except:
                if settings.do_logs:
                    __globals__.logger.warn(
                        f'Failed to convert input {self.input} to bytes / chars')
        # Send string input
        else:
            SerialIO.run(__globals__.serial, 'write', self.input.encode())
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
