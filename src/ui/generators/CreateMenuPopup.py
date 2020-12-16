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

from ui import getPath

from PyQt5.QtWidgets import QMenu, QAction


class CreateMenuPopup():
    def __init__(self, parent=None):
        self.parent = parent

    def makeMenu(self):
        self.menu = QMenu(self.parent)
        with open(getPath('main_ld.qss'), 'r') as style_file:
            self.menu.setStyleSheet(style_file.read())
        return(self.menu)

    def addOption(self, menu, option_name, option_payload, highlighted=False):
        self.option_name = option_name
        self.action = QAction(option_name, self.parent)
        self.action.triggered.connect(lambda: self.runFunction(option_payload))
        menu.addAction(self.action)
        # Set entry style as highlighted
        if highlighted:
            menu.setDefaultAction(self.action)
