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


class SolidColour():
    def __init__(self, *args, **kwargs):
        self.getColour()

    def getColour(self):
        # self.handleButton()
        Globals.colour_picker.exec()
        self.current_colour = Globals.colour_picker.currentColor().getRgb()
        print(self.current_colour)

    @staticmethod
    def effectData():
        effect_name = 'Solid Colour'
        return effect_name
