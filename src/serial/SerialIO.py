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

from time import sleep

from src import __globals__
from src import settings

from src.rw.jsonio import JsonIO

from src.serial.serial_worker import SerialWorker

from PyQt5.QtCore import QIODevice, QThread
from PyQt5.QtSerialPort import QSerialPort


class SerialIO():
    def __init__(self, port, baudrate=None):
        # Initialise serial communication
        __globals__.serial = QSerialPort(port, baudRate=baudrate)
        try:
            if not __globals__.serial.isOpen():
                __globals__.serial.open(QIODevice.ReadWrite)
        except:
            pass
        # Get data from board
        SerialIO.run('getBoardInfo')

    @staticmethod
    def run(target_method, *args, **kwargs):
        if not __globals__.serial_thread.isRunning():
            serial = __globals__.serial
            method = getattr(SerialIO, target_method)
            worker = SerialWorker()
            thread = QThread()
            worker.ready.connect(lambda: method(serial, *args, **kwargs))
            worker.moveToThread(thread)
            worker.finished.connect(thread.quit)
            thread.started.connect(worker.procCounter)
            __globals__.serial_thread = thread
            thread.start()
            # This sleep enables the thread to run
            # Otherwise the thread starts but does not execute anything
            sleep(1/1000000)
            # Without this print, the thread sometimes decides not to quit ¯\_(ツ)_/¯
            print('Thread started')
            if settings.do_logs:
                __globals__.logger.info(
                    f'Thread {__globals__.serial_thread} started')
        else:
            __globals__.logger.warn(
                'Serial communication already running (Thread already exists)')

    @staticmethod
    def write(serial, message, out_type=None, *args, **kwargs):
        if out_type is None:
            serial.write(message)
        # UINT8_T output
        elif out_type == 'Integer':
            try:
                # Split input for multiple args
                input_array = message.split(',')
                input_array = [int(item) for item in input_array]
                input_array = bytearray(input_array)
                serial.write(input_array)
            except:
                if settings.do_logs:
                    __globals__.logger.warn(
                        f'Failed to convert input {message} to bytearray')
        # UINT8_T + char output
        elif out_type == 'Integer-Char':
            try:
                # Split string and integer parts
                input_array = message.split(',')
                output_bytes = b''
                for entry in input_array:
                    if entry:
                        try:
                            entry = int(entry).to_bytes(1, byteorder='big')
                        except ValueError:
                            entry = entry.encode()
                        output_bytes += entry
                serial.write(bytearray(output_bytes))
            except:
                if settings.do_logs:
                    __globals__.logger.warn(
                        f'Failed to convert input {message} to bytes / chars')
        # Formatted output for ArduRGB device
        elif out_type == 'ArduRGB':
            try:
                # Split string and integer parts
                input_array = message.split(',')
                # Serial start byte 255
                output_bytes = b'\xfe'
                # Add strip number
                output_bytes += __globals__.current_strip.to_bytes(
                    1, byteorder='big')
                for entry in input_array:
                    if entry:
                        try:
                            # UINT8_T effect arg
                            entry = int(entry).to_bytes(1, byteorder='big')
                        except ValueError:
                            # String literal string effect name
                            output_bytes += len(entry).to_bytes(1,
                                                                byteorder='big')
                            entry = entry.encode()
                        output_bytes += entry
                # Serial end byte 254
                output_bytes += b'\xff'
                serial.write(bytearray(output_bytes))
            except:
                if settings.do_logs:
                    __globals__.logger.warn(
                        f'Failed to convert input {message} to bytes / chars')
        # Raw string output
        elif out_type == 'String':
            serial.write(message.encode())
        # Invalid output
        elif settings.do_logs:
            __globals__.logger.warn(
                f'Message output type {out_type} not defined')

    @staticmethod
    def read(serial, *args, **kwargs):
        data = data = serial.readAll().data()
        try:
            data = data.decode()
            return data
        except:
            if settings.do_logs:
                __globals__.logger.warn(
                    f'Could not decode serial input {data}')

    @staticmethod
    def getBoardInfo(serial, *args, **kwargs):
        serial.write(bytearray(b'\xfe\x00\tboardinfo\xff'))
        # Store number of lines read from serial
        __globals__.board_data_lines = 0
        # Store multiple message lines in one message
        __globals__.board_data_buffer = ''
        # Read serial when available
        serial.readyRead.connect(SerialIO.setBoardInfo)

    @classmethod
    def setBoardInfo(cls):
        __globals__.board_data_buffer += SerialIO.read(__globals__.serial)
        # Finished reading data
        if __globals__.board_data_lines:
            # Disconnect slot
            __globals__.serial.readyRead.disconnect(SerialIO.setBoardInfo)
            # Create list of board data
            serial_data = __globals__.board_data_buffer
            serial_data = serial_data.strip('\r\n').split(',')
            # Ensure received message contains all data
            try:
                # Get relevant data
                if len(serial_data) == int(serial_data[0]) + 1:
                    board_data = {'name': serial_data[1],
                                  'type': serial_data[2],
                                  'version': serial_data[3],
                                  'physical_strips': serial_data[4],
                                  'virtual_strips': serial_data[5],
                                  'default_brightness': serial_data[6],
                                  'port': __globals__.serial.portName()}
                    __globals__.board_data = board_data
                    __globals__.comm_module = [__name__, cls.__name__]
                    command = {'type': 'serial',
                               'payload': __globals__.serial.portName()}
                    JsonIO('devices.json').writeEntry('known_devices', 'devices',
                                                      serial_data[1], serial_data[1], command, sort_keys=True)
                    # Update brightness slider
                    __globals__.parent.ui.slider_brightness.setValue(
                        int(serial_data[6]))

                    # Create LED strips menu
                    def initStripsMenu():
                        from src.ui.generators.create_menu_context import CreateMenuContext
                        from PyQt5.QtGui import QCursor
                        ContextMenuGen = CreateMenuContext(
                            parent=__globals__.parent)
                        # Create menu
                        __globals__.popup_view = ContextMenuGen.makeMenu()
                        popup_view = ContextMenuGen.makeMenu()
                        # Add entries
                        try:
                            for i in range(int(serial_data[5])):
                                # Set highlighted entry
                                if i == __globals__.current_strip:
                                    ContextMenuGen.addOption(
                                        popup_view, f'LED Strip {i}', (None, ('selectStrip', i)), highlighted=True)
                                # Set non-highlighted entry
                                else:
                                    ContextMenuGen.addOption(
                                        popup_view, f'LED Strip {i}', (None, ('selectStrip', i)))
                        except:
                            pass
                        # Show menu
                        popup_view.exec(QCursor.pos())
                    # Show strips menu when clicked
                    __globals__.strips_menu.clicked.connect(initStripsMenu)
                else:
                    if settings.do_logs:
                        __globals__.logger.warn(
                            f'Serial input {serial_data[1:]} not of expected size {serial_data[0]}')
            except:
                if settings.do_logs:
                    __globals__.logger.warn(
                        f'Expected type integer, instead got {serial_data[0]}')
        # Read next line from serial - message sent in two lines
        else:
            __globals__.board_data_lines += 1
