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
import setuptools
from pathlib import Path

path = Path(__file__).parent.resolve()

# Get version data
__version__ = (path / '__version__.py').read_text(encoding='utf-8')
python_version = sys.version_info[:2]
python_requires = None
prog_version = None
for line in __version__.split('\n'):
    if '__version__' in line:
        prog_version = line.strip("__version__ ='")
    elif 'python_requires' in line:
        requires_as_str = line.strip(
            "python_requires ='").strip('()').split(', ')
        python_requires = (int(requires_as_str[0]), int(requires_as_str[1]))

# Enforce version
if python_version < python_requires:
    sys.stderr.write(f"""
    ==========================
    Unsupported Python version
    ==========================

    Your system is running Python {python_version[0]}.{python_version[1]}
    which is lower than the required Python {python_requires[0]}.{python_requires[1]}.

    Please consider updating your installation.
    """)
    sys.exit(1)

setuptools.setup()
