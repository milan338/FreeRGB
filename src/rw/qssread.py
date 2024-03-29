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
from src import settings

from os.path import abspath, dirname, join


class QssRead():
    def __init__(self, file):
        # Initialise path
        self.base_path = abspath(dirname(__file__))
        self.styles_dir = 'ui/styles'
        self.styles_path = abspath(join(self.base_path, '..', self.styles_dir))
        # Set up final file to load
        self.file_path = abspath(join(self.styles_path, f'{file}.qss'))
        self.final_path = abspath(join(self.styles_path, f'{file}_ld.qss'))
        self.writeLines()

    def writeLines(self):
        # Get file lines
        with open(self.file_path, 'r') as in_file:
            self.file_lines = in_file.readlines()
        with open(self.final_path, 'w') as out_file:
            out_file.write(
                '/*FILE GENERATED BY FREERGB QSS PARSER\nANY CHANGES MADE HERE WILL BE LOST ON NEXT STARTUP*/\n\n')
            # Search for imports
            for line in self.file_lines:
                try:
                    if line.startswith('@import'):
                        self.import_name = (line.split(
                            '@import')[1].replace("'", "").replace(';', '').strip('\r\n').split()[0])
                        self.import_path = abspath(
                            join(self.styles_path, self.import_name))
                        self.new_lines = self.readFile(self.import_path)
                        out_file.writelines(self.new_lines)
                    else:
                        out_file.write(line)
                except:
                    if settings.do_logs:
                        __globals__.logger.error(
                            f'Failed to parse stylesheet line [{line}]')

    def readFile(self, path):
        with open(path, 'r') as import_file:
            self.import_lines = import_file.readlines()
        self.out_lines = []
        # Remove license header - assumes license header occupies first comment
        self.in_header = 0
        for line in self.import_lines:
            if self.in_header == 0 and line.startswith('/*'):
                self.in_header = 1
            elif self.in_header == 1 and line.startswith('*/'):
                self.in_header = -1
            elif self.in_header == -1:
                self.out_lines.append(line)
        return self.out_lines
