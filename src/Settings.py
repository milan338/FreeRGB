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

from rw.JsonIO import JsonIO

# Store settings
advanced_mode = None
update_check = None
do_logs = None
startup_run = None
background_activity = None


# Load settings from disk
def reloadSettings():
    ld_settings = JsonIO('settings.json').readEntry('settings')
    settings = ld_settings['settings_button_layout']
    for option_name, option_contents in settings.items():
        # Ensure option is toggle
        if option_contents['command']['type'] == 'toggleBool':
            # Update each option with value from file
            globals()[option_name] = option_contents['command']['payload']
            # Change visibility of advanced mode elements
            if option_name == 'advanced_mode':
                setAdvancedModeVisible()


def setAdvancedModeVisible():
    global advanced_mode
    for element in Globals.advanced_mode_elements:
        element.setVisible(advanced_mode)
