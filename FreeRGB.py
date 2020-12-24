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

import sys
import __version__

from src import __main__

if __name__ == '__main__':
    curr_version = sys.version_info
    min_py = __version__.python_requires.split('.')
    # Ensure Python installation meets requirements
    if curr_version >= (int(min_py[0]), int(min_py[1])):
        __main__.init()
    else:
        from src import __globals__
        from src.init_logging import InitLogging
        InitLogging(2)
        __globals__.logger.error(
            f'Your system running Python {curr_version[0]}.{curr_version[1]}'
            f' which is lower than the required Python {min_py[0]}.{min_py[1]}.'
            f' Please consider updating your installation.')
