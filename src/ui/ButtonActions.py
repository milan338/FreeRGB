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

import Globals
import Settings

from ui import getPath
from ui.views.licenses.LicensesView import LicensesView

from webbrowser import open as openWebPage


class ButtonActions():
    @staticmethod
    def toggleBool(*args, **kwargs):
        # Reload settings
        Settings.reloadSettings()

    @staticmethod
    def openURL(url, *args, **kwargs):
        openWebPage(url)

    @staticmethod
    def showLicenses(*args, **kwargs):
        Globals.licenses_view = LicensesView()
        Globals.licenses_view.setWindowTitle('Open-Source Licenses')
        Globals.licenses_view.show()
        # Globals.licenses_view.setWindowIcon()
