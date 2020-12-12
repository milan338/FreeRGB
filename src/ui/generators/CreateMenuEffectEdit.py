import Globals

from ui.GenerateButtons import GenerateButtons
from ui.generators.CreateMenuPopup import CreateMenuPopup


class CreateMenuEffectEdit(CreateMenuPopup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def runFunction(self, function_name):
        try:
            getattr(GenerateButtons('menus.json', 'main_menu_right_click_menu'), function_name)(
                Globals.current_hovered_btn)
            # Refresh menu layout using JSON
            Globals.refreshMenus()
        except:
            print('exception')
