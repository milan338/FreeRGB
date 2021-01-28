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


def run(*args, **kwargs):
    print('run')
    # Import file
    try:
        import_path = __globals__.comm_module[0]
        import_class = __globals__.comm_module[1]
        module = __import__(import_path, fromlist=[None])
        module_class = getattr(module, import_class)
        # Run communication method
        getattr(module_class, 'run')(*args, **kwargs)
    except:
        if settings.do_logs:
            __globals__.logger.error(
                f'Failed to import / run {__globals__.comm_module[0]}')
