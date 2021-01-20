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

import webbrowser

from src import __globals__
from src import settings

from src.ui.views.licenses.licenses_view import LicensesView


class ButtonActions():
    @staticmethod
    def toggleBool(*args, **kwargs):
        # Reload settings
        settings.reloadSettings()

    @staticmethod
    def openURL(url, *args, **kwargs):
        webbrowser.open(url)

    @ staticmethod
    def showLicenses(*args, **kwargs):
        __globals__.popup_view = LicensesView()
        __globals__.popup_view.setWindowTitle('Open-Source Licenses')
        __globals__.popup_view.show()
        # Globals.licenses_view.setWindowIcon()
