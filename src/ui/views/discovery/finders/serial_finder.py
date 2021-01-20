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

from src.ui.views.discovery.finders.base_finder import BaseFinder

from PyQt5.QtSerialPort import QSerialPortInfo


class SerialFinder(BaseFinder):
    def __init__(self):
        super().__init__()
        # Get available ports
        self.port_list = [
            serial_port for serial_port in QSerialPortInfo.availablePorts()]
        # Add devices
        for port in self.port_list:
            self.port_name = (f'{port.portName()}\n\n'
                              f'{port.description()}\n'
                              f'Manufacturer: {port.manufacturer()}\n'
                              f'Product ID: {port.productIdentifier()}\n'
                              f'Vendor ID: {port.vendorIdentifier()}')
            self.addDevice(self.port_name, 'connectSerial', port.portName())
