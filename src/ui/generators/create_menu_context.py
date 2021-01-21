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

from src.ui.button_actions import ButtonActions
from src.ui.generators.create_menu_popup import CreateMenuPopup


class CreateMenuContext(CreateMenuPopup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def runFunction(self, args):
        self.dropdown_menu = args[0]
        self.selection = args[1]
        # Dropdown menu where selection does not immediately call function
        if self.dropdown_menu:
            # Change text of button if button features text
            self.dropdown_menu.setText(self.option_name)
            # Store selection in buffer
            __globals__.popup_menu_selection = self.selection
        # Context menu where selection immediately calls function
        else:
            self.command = self.selection[0]
            self.args = self.selection[1]
            getattr(ButtonActions, self.command)(self.args)
