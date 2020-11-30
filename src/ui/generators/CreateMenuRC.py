import Globals

from ui.GenerateButtons import GenerateButtons

from PyQt5.QtWidgets import QMenu, QAction


class CreateMenuRC():
    def __init__(self, parent=None,):
        self.parent = parent

    def makeMenu(self, style_sheet):
        self.menu = QMenu(self.parent)
        # Set style
        with open(style_sheet) as style_file:
            self.menu.setStyleSheet(style_file.read())
        return(self.menu)

    def addOption(self, menu, option_name, option_payload):
        self.action = QAction(option_name, self.parent)
        self.action.triggered.connect(lambda: self.runFunction(option_payload))
        menu.addAction(self.action)

    def runFunction(self, function_name):
        getattr(GenerateButtons('menus.json', 'main_menu_right_click_menu'), function_name)(
            Globals.current_hovered_btn)
        try:
            getattr(GenerateButtons('right_click_menu.json', 'main_menu_right_click_menu'), function_name)(
                Globals.current_hovered_btn)
        except:
            print('exception')
