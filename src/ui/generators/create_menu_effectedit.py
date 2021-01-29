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

from src.ui.generate_buttons import GenerateButtons
from src.ui.generators.create_menu_popup import CreateMenuPopup


class CreateMenuEffectEdit(CreateMenuPopup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def runFunction(self, method_name):
        try:
            # Run static method
            if type(GenerateButtons.__dict__[method_name]) == staticmethod:
                getattr(GenerateButtons, method_name)()
            # Run method
            else:
                getattr(GenerateButtons('menus.json',
                                        'main_menu'), method_name)()
        except:
            if settings.do_logs:
                __globals__.logger.error(
                    f'Failed to call method {method_name} with argument {__globals__.current_hovered_btn}'
                    f' from module src.ui.GenerateButtons')
