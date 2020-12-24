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

from pathlib import Path

path = Path(__file__).parent.resolve()
__version__ = (path / '__version__.py').read_text(encoding='utf-8')

version = None
python_requires = None

for line in __version__.split('\n'):
    if '__version__' in line:
        version = line.strip("__version__ ='")
    elif 'python_requires' in line:
        python_requires = line.strip("python_requires ='")