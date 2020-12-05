from rw.JsonIO import JsonIO

from ui.views.input.InputDialogue import InputDialogue
from ui.generators.CreateLargeButton import CreateLargeButton


class GenerateButtons():
    def __init__(self, file, page):
        self.file = file
        self.page_contents = JsonIO(file).readEntry(page)

    def generateGenericButtons(self, vertical_element, scroll_element, style_sheet, right_click_menu, spacer=False):
        for elements in self.page_contents.values():
            for element, attributes in elements.items():
                self.btn = CreateLargeButton(vertical_element, spacer=spacer).createGenericButton(
                    attributes['text'], element, scroll_element, style_sheet, right_click_menu)

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
                    pass

    def editButton(self, button):
        # self.initDialogue(
        #     'serial_direct', 'main_menu', 'Create New Effect')
        # self.input_dialogue = InputDialogue('serial_direct', 'main_menu', 'Edit Effect')
        print('tmp')

    def deleteButton(self, button):
        JsonIO(self.file).removeEntry(button.objectName())

    def moveButtonUp(self, button):
        JsonIO(self.file).shiftEntry(button, -1)

    def moveButtonDown(self, button):
        JsonIO(self.file).shiftEntry(button, 1)
