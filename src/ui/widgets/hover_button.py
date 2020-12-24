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

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal


# QPushButton that detects when hovered
class HoverButton(QPushButton):
    mouse_hovered = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.mouse_hovered.emit(True)

    def leaveEvent(self, event):
        self.mouse_hovered.emit(False)
