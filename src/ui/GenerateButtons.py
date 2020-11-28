from ui.Ui_MainWindow import Ui_Form

from rw.JsonIO import JsonIO

from ui.widgets.CreateLargeButton import CreateLargeButton


class GenerateButtons():
    def __init__(self, page):
        self.page_contents = JsonIO('menus.json').readEntry(page)

    def generateGenericButtons(self, vertical_element, scroll_element, style_sheet, right_click_menu, spacer=False):
        for layout, elements in self.page_contents.items():
            for element, attributes in elements.items():
                CreateLargeButton(vertical_element, spacer=spacer).createGenericButton(
                    attributes['text'], element, scroll_element, style_sheet, right_click_menu)
                # for attribute_name, attribute_value in attributes.items():

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
