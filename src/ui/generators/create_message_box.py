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
from src import settings

from src.rw.jsonio import JsonIO

from PyQt5.QtWidgets import QMessageBox


class CreateMessageBox():
    def __init__(self, title, prompt, parent=None,):
        self.title = title
        self.prompt = prompt
        self.parent = parent
        self.message_box = QMessageBox

    def getBool(self):
        self.input = self.message_box.question(
            self.parent, self.title, self.prompt, self.message_box.Yes | self.message_box.No)
        # Return True for yes and False for no
        return self.input == self.message_box.Yes

    def confirmDelete(self):
        return self.getBool()

    def resetPreferences(self, file, menu=None, layout=None, reset_file=False, reload_settings=False):
        # Get input from user and continue only if input was 'yes'
        if self.getBool():
            if reset_file:
                JsonIO(file).copyFromBase()
            else:
                JsonIO(file).copyLayout(menu, layout)
            # Reload settings
            if reload_settings:
                settings.reloadSettings()
            # Refresh menu button layout using JSON
            __globals__.refreshMenus()
