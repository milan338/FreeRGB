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

def initStripsMenu(data):
    from src.ui.generators.create_menu_context import CreateMenuContext
    from PyQt5.QtGui import QCursor
    ContextMenuGen = CreateMenuContext(
        parent=__globals__.parent)
    # Create menu
    __globals__.popup_view = ContextMenuGen.makeMenu()
    popup_view = ContextMenuGen.makeMenu()
    # Add entries
    try:
        for i in range(data):
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
