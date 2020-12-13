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
# along with FreeRGB. If not, see <https://www.gnu.org/licenses/>.

import Globals

from ui.generators.CreateMenuPopup import CreateMenuPopup


class CreateMenuContext(CreateMenuPopup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def runFunction(self, args):
        self.button_with_text = args[0]
        self.selection = args[1]
        # Change text of button if button features text
        if self.button_with_text:
            self.button_with_text.setText(self.option_name)
        # Store selection in buffer
        Globals.popup_menu_selection = self.selection
