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

    def removeButtons(self, layout):
        for i in reversed(range(layout.count())):
            # Attempt to remove spacer item
            try:
                layout.itemAt(i).removeItem()
            except:
                # Attempt to remove widget
                try:
                    layout.takeAt(i).widget().deleteLater()
                except:
                    if settings.do_logs:
                        __globals__.logger.error(
                            f'Failed to remove UI element in layout {layout.objectName()}'
                            f' at UI position {layout.count() - i}')

    def editButton(self, button):
        # Reset input window
        __globals__.edit_effect_menu = None
        # Set up input window
        __globals__.edit_effect_menu = InputDialogue(
            'main_menu', new_entry=False, btn_name=button.objectName())
        __globals__.edit_effect_menu.setWindowTitle('Edit Effect')
        __globals__.edit_effect_menu.show()

    def deleteButton(self, button):
        # Delete button if user confirms in message box
        if CreateMessageBox('Delete Effect', 'This action will remove this button. Continue?').confirmDelete():
            JsonIO(self.file).removeEntry(button.objectName())

    def moveButtonUp(self, button):
        JsonIO(self.file).shiftEntry(button, -1)

    def moveButtonDown(self, button):
        JsonIO(self.file).shiftEntry(button, 1)
