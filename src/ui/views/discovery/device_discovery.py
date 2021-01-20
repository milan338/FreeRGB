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

from src.ui import getPath

from src.ui.views.discovery.Ui_device_discovery import Ui_Form
from src.ui.views.discovery.finders.serial_finder import SerialFinder

from PyQt5.QtWidgets import QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt


class DeviceDiscovery(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Setup UI
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # Block inputs to application while dialogue active
        self.setWindowModality(Qt.ApplicationModal)
        # Set style sheet
        with open(getPath('main_ld.qss'), 'r') as style_file:
            self.setStyleSheet(style_file.read())

    def findDevices(self):
        SerialFinder()

    def addDevices(self):
        # Imports done here to prevent circular imports
        from src.ui.generate_buttons import GenerateButtons
