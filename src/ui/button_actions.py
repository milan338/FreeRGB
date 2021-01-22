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


class ButtonActions():
    @staticmethod
    def toggleBool(*args, **kwargs):
        settings.reloadSettings()

    @staticmethod
    def openURL(url, *args, **kwargs):
        webbrowser.open(url)

    @staticmethod
    def showLicenses(*args, **kwargs):
        from src.ui.views.licenses.licenses_view import LicensesView
        __globals__.popup_view = LicensesView()
        __globals__.popup_view.setWindowTitle('Open-Source Licenses')
        __globals__.popup_view.show()
        # Globals.licenses_view.setWindowIcon()

    @staticmethod
    def connectSerial(port, *args, **kwargs):
        from src.serial.serialio import SerialIO
        SerialIO(port).run(__globals__.serial, 'getBoardInfo')

    @staticmethod
    def selectStrip(strip, *args, **kwargs):
        from src.rw.jsonio import JsonIO
        __globals__.current_strip = strip
        # Clear existing strip
        JsonIO('devices.json').blankCopy(
            'selected_device', 'strips', dump=True)
        # Write new strip
        JsonIO('devices.json').writeRaw('selected_device', 'strips',
                                        strip, None, sort_keys=True)

    @staticmethod
    def selectDevice(device, *args, **kwargs):
        from src.serial.serialio import SerialIO
        from src.rw.jsonio import JsonIO
        device_name = device[0]
        device_attributes = device[1]
        # Clear existing device
        JsonIO('devices.json').blankCopy(
            'selected_device', 'devices', dump=True)
        # Write new device
        JsonIO('devices.json').writeRaw('selected_device', 'devices',
                                        device_name, device_attributes, sort_keys=True)
        # Set new communcation type
        comm_type = device_attributes['command']['type']
        comm_port = device_attributes['command']['payload']
        # Initialise communication
        comm_objects = {
            'serial': SerialIO}
        comm_globals = [
            'serial']
        disable_strips = []
        try:
            # Init device communication
            comm_objects[comm_type](comm_port)
            # Display debugging tools if previously disabled from invalid device
            if settings.advanced_mode:
                settings.setAdvancedModeVisible(override=True)
            # Disable strips menu
            if comm_type in disable_strips:
                __globals__.strips_menu.setVisible(False)
            else:
                __globals__.strips_menu.setVisible(True)
        except:
            if settings.do_logs:
                __globals__.logger.error(
                    f'Failed to initialise {comm_type} communication through {comm_port}')
            # Set all communications to None
            for global_var in comm_globals:
                setattr(__globals__, global_var, None)
            # Clear global board data
            __globals__.board_data = {'name': None,
                                      'type': None,
                                      'port': None}
            # Disable strips menu
            __globals__.strips_menu.setVisible(False)
            # Disable debugging tools
            settings.setAdvancedModeVisible(override=False)
