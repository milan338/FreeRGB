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

from src.init_logging import InitLogging

from src.rw.jsonio import JsonIO

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
            options = {
                'advanced_mode': setAdvancedModeVisible,
                'do_logs': initLogs
            }
            # Run function associated with option
            if option_name in list(options.keys()):
                options.get(option_name)()


def setAdvancedModeVisible(override=None):
    global advanced_mode
    if not override is None:
        for element in __globals__.advanced_mode_elements:
            element.setVisible(override)
    else:
        for element in __globals__.advanced_mode_elements:
            element.setVisible(advanced_mode)


def initLogs(have_init=[]):
    global do_logs
    # If logs have not been initialised in session
    if do_logs and not have_init:
        InitLogging(2)
        have_init.append(1)
