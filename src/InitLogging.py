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

import logging

from src import Globals

from datetime import datetime

from logging.handlers import RotatingFileHandler

from os import makedirs, listdir, remove
from os.path import abspath, dirname, join, isdir, isfile, getmtime

from zipfile import ZipFile


class InitLogging():
    def __init__(self, max_logs, name):
        self.max_logs = max_logs
        self.name = name
        self.backup_count = 2
        self.base_path = abspath(dirname(__file__))
        self.log_dir = 'logs'
        self.log_latest = 'latest.log'
        self.log_path = abspath(join(self.base_path, '..', self.log_dir))
        self.latest_path = abspath(join(self.log_path, self.log_latest))
        # Store previous log
        if isdir(self.log_path):
            if isfile(self.latest_path):
                self.storeLog()
        else:
            makedirs(self.log_path)
        self.createLog()

    def storeLog(self):
        self.backup_ext = ['.log'] + \
            [f'.log.{i}' for i in list(range(1, self.backup_count + 1))]
        self.files = []
        self.zip_files = {}
        # Get log modified time
        self.modify_time = datetime.fromtimestamp(
            getmtime(self.latest_path)).strftime('%Y-%m-%d_%H-%M-%S')
        with ZipFile(abspath(join(self.log_path, f'{self.modify_time}.log.zip')), 'w') as zip_file:
            # Go through files in directory
            for file in listdir(self.log_path):
                file_path = abspath(join(self.log_path, file))
                if isfile(file_path):
                    # Check for log files
                    if file.endswith(tuple(self.backup_ext)):
                        zip_file.write(file_path, file)
                        self.files.append(file_path)
                    # Find existing logs
                    elif file.endswith('.zip'):
                        self.zip_files.update(
                            {file_path: getmtime(file_path)})
        # Remove files added to zip
        for file in self.files:
            remove(file)
        # Truncate logs directory if past size limit
        while len(self.zip_files) > self.max_logs:
            # Remove oldest file
            self.oldest_zip = min(self.zip_files, key=self.zip_files.get)
            del self.zip_files[self.oldest_zip]
            remove(self.oldest_zip)

    def createLog(self):
        self.formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)-s :: %(filename)s in %(funcName)s on line %(lineno)d :: %(message)s')
        # self.logger = logging.getLogger('main_logger')
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.WARNING)
        # Enable logging to file, where each 5MB the log rolls over to a new file
        self.file_handler = RotatingFileHandler(
            self.latest_path, maxBytes=5*1024*1024, backupCount=self.backup_count)
        # Enable logging to console
        self.console_handler = logging.StreamHandler()
        # Apply logger formatters
        self.file_handler.setFormatter(self.formatter)
        self.console_handler.setFormatter(self.formatter)
        # Apply handlers to logger
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)
        # Provide application-wide access to logger
        Globals.logger = self.logger
