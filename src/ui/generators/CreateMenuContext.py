import Globals

from ui.generators.CreateMenuPopup import CreateMenuPopup


class CreateMenuContext(CreateMenuPopup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def runFunction(self, args):
        self.button_with_text = args[0]
        self.selection = args[1]
        # Change text of button if button features text
        if self.button_with_text:
            self.button_with_text.setText(self.option_name)
        # Store selection in buffer
        Globals.popup_menu_selection = self.selection
