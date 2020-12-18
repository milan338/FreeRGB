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

from src import Globals

from src.ui.GenerateButtons import GenerateButtons
from src.ui.generators.CreateMenuPopup import CreateMenuPopup


class CreateMenuEffectEdit(CreateMenuPopup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def runFunction(self, function_name):
        try:
            getattr(GenerateButtons('menus.json', 'main_menu_right_click_menu'), function_name)(
                Globals.current_hovered_btn)
            # Refresh menu layout using JSON
            Globals.refreshMenus()
        except:
            print('exception')
