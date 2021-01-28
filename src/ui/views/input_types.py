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

from src import __globals__

from src.ui.generators.create_menu_context import CreateMenuContext

from PyQt5.QtGui import QCursor, QRegExpValidator
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import pyqtSlot, QRegExp


class InputTypes():
    def genValidators(self, button, entry):
        self.button = button
        self.entry = entry
        # Menu to select validator type
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
                            'ArduRGB': self.int_char_validator,
                            'String': None}
        self.button.clicked.connect(self.initTypeMenu)
        self.selected_type = 'Integer'
        self.button.setText('Input: Integer')
        self.entry.setValidator(self.int_validator)

    def initTypeMenu(self):
        self.input_menu.clear()
        for input_type, validator_type in self.input_types.items():
            if input_type == self.selected_type:
                CreateMenuContext(parent=self).addOption(
                    self.input_menu, input_type, (self.button, validator_type), highlighted=True)
            else:
                CreateMenuContext(parent=self).addOption(
                    self.input_menu, input_type, (self.button, validator_type))
        self.input_menu.exec(QCursor.pos())

    @pyqtSlot(QAction)
    def updateInputType(self, action):
        self.selected_type = action.text()
        self.button.setText(f'Input: {self.selected_type}')
        self.entry.setValidator(
            __globals__.popup_menu_selection)
        self.entry.clear()
