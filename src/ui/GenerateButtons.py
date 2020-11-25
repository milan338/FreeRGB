from ui.Ui_MainWindow import Ui_Form

from rw.JsonIO import JsonIO

from ui.widgets.LargeButton import CreateLargeButton

from PyQt5 import QtWidgets


class GenerateButtons():
    def __init__(self, page):
        self.page_contents = JsonIO('menus.json').readEntry(page)

    def generateGenericButtons(self, vertical_element, scroll_element, style_sheet, spacer=False):
        for layout, elements in self.page_contents.items():
            for element, attributes in elements.items():
                CreateLargeButton(vertical_element, spacer=spacer).createGenericButton(
                    attributes['text'], element, scroll_element, style_sheet)
                # for attribute_name, attribute_value in attributes.items():
