import Globals

import logging

from datetime import datetime

from logging.handlers import RotatingFileHandler

from os import path, makedirs, listdir, remove

from zipfile import ZipFile


class InitLogging():
    def __init__(self, max_logs):
        self.max_logs = max_logs
        self.backup_count = 2
        self.base_path = path.dirname(__file__)
        self.log_dir = 'logs'
        self.log_latest = 'latest.log'
        self.log_path = path.abspath(
            path.join(self.base_path, '..', self.log_dir))
        self.latest_path = path.join(self.log_path, self.log_latest)
        # Store previous log
        if path.isdir(self.log_path):
            if path.isfile(self.latest_path):
                self.storeLog()
        else:
            makedirs(self.log_path)
        self.createLog()

    def storeLog(self):
        self.backup_ext = [
            '.log'] + [f'.log.{i}' for i in list(range(1, self.backup_count + 1))]
        self.files = []
        # Get log modified time
        self.modify_time = datetime.fromtimestamp(
            path.getmtime(self.latest_path)).strftime('%Y-%m-%d_%H-%M')
        with ZipFile(path.join(self.log_path, f'{self.modify_time}.log.zip'), 'w') as zip_file:
            # Go through files in directory
            for file in listdir(self.log_path):
                file_path = path.join(self.log_path, file)
                if path.isfile(file_path):
                    # Check for log files
                    if file.endswith(tuple(self.backup_ext)):
                        zip_file.write(file_path, file)
                        self.files.append(file_path)
        # Remove files added to zip
        for file in self.files:
            remove(file)

    def createLog(self):
        # self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcname)s %(lineno)d %(message)s')
        self.logger = logging.getLogger('main_logger')
        self.logger.setLevel(logging.WARNING)
        self.handler = RotatingFileHandler(
            self.latest_path, maxBytes=5*1024*1024, backupCount=self.backup_count)
        self.logger.addHandler(self.handler)
        # logging.basicConfig(filename=self.latest_path)
        # Provide application-wide access to logger
        Globals.logger = self.logger
