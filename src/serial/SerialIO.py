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

from src.serial.serial_worker import SerialWorker

from PyQt5.QtCore import QIODevice, QThread, pyqtSlot
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo


class SerialIO():
    def __init__(self, port, baudrate):
        self.baudrate = baudrate
        __globals__.serial = QSerialPort(port, baudRate=baudrate)
        self.port_list = [serial_port.portName()
                          for serial_port in QSerialPortInfo.availablePorts()]
        try:
            if not __globals__.serial.isOpen():
                __globals__.serial.open(QIODevice.ReadWrite)
        except:
            pass

        print(self.port_list)
        SerialIO.run(__globals__.serial, 'getBoardInfo', __globals__.serial)

    @staticmethod
    def run(serial, target_method, *args, **kwargs):
        if not __globals__.serial_thread.isRunning():
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
    def write(serial, message, *args, **kwargs):
        serial.write(message)

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

    @staticmethod
    @pyqtSlot()
    def setBoardInfo():
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
                    board_data = {'type': serial_data[2],
                                  'version': serial_data[3],
                                  'physical_strips': serial_data[4],
                                  'virtual_strips': serial_data[5],
                                  'default_brightness': serial_data[6]}
                    # Key represents user defined board name
                    __globals__.board_data.append({serial_data[1]: board_data})
                    print(__globals__.board_data)
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
