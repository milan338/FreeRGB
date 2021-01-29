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

from src.rw.jsonio import JsonIO

from src.ui.views.input.input_dialogue import InputDialogue
from src.ui.generators.create_large_button import CreateLargeButton
from src.ui.generators.create_message_box import CreateMessageBox


class GenerateButtons():
    def __init__(self, file, page):
        self.file = file
        self.page_contents = JsonIO(file).readEntry(page)
        self.button = __globals__.current_hovered_btn

    def generateGenericButtons(self, vertical_element, scroll_element, style, right_click_menu=None, spacer=False, effect_btn=False):
        for elements in self.page_contents.values():
            for element_name, element_attributes in elements.items():
                # Create toggle button
                if element_attributes['command']['type'] == 'toggleBool':
                    self.btn = CreateLargeButton(vertical_element, spacer=spacer).createToggleButton(
                        element_name, element_attributes, scroll_element, style)
                # Create pushbutton
                else:
                    self.btn = CreateLargeButton(vertical_element, spacer=spacer, effect_btn=effect_btn).createGenericButton(
                        element_name, element_attributes, scroll_element, style, right_click_menu)

    @staticmethod
    def removeButtons(layout):
        for i in reversed(range(layout.count())):
            try:
                widget = layout.takeAt(i).widget()
                item = layout.itemAt(i)
                # Remove widget
                if widget:
                    widget.deleteLater()
                # Remove spacer item
                elif item:
                    item.removeItem()
            except:
                if settings.do_logs:
                    __globals__.logger.error(
                        f'Failed to remove UI element in layout {layout.objectName()}'
                        f' at UI position {i}')

    @staticmethod
    def editButton():
        button = __globals__.current_hovered_btn
        # Reset input window
        __globals__.popup_view = None
        # Set up input window
        __globals__.popup_view = InputDialogue(
            'main_menu', new_entry=False, btn_name=button.objectName())
        __globals__.popup_view.setWindowTitle('Edit Effect')
        __globals__.popup_view.show()

    def deleteButton(self):
        # Delete button if user confirms in message box
        if CreateMessageBox('Delete Effect', 'This action will remove this button. Continue?').confirmDelete():
            JsonIO(self.file).removeEntry(self.button.objectName())
        # Refresh menu
        __globals__.refreshMenus()

    def moveButtonUp(self):
        JsonIO(self.file).shiftEntry(self.button, -1)
        # Refresh menu
        __globals__.refreshMenus()

    def moveButtonDown(self):
        JsonIO(self.file).shiftEntry(self.button, 1)
        # Refresh menu
        __globals__.refreshMenus()

    def deviceDiscovery(self, *args, **kwargs):
        from src.ui.views.discovery.device_discovery import DeviceDiscovery
        # Reset input window
        __globals__.popup_view = None
        __globals__.popup_view = DeviceDiscovery()
        __globals__.popup_view.setWindowTitle('Device Discovery')
        __globals__.popup_view.show()
