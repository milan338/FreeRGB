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

from PyQt5.QtCore import QIODevice, QThread
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
        data = serial.readAll().data().decode()
        return data

    def getBrightness(self):
        print('tmp')
