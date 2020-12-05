import Globals

from rw.JsonIO import JsonIO

from PyQt5.QtWidgets import QMessageBox


class CreateMessageBox():
    def __init__(self, title, prompt, parent=None,):
        self.title = title
        self.prompt = prompt
        self.parent = parent
        self.message_box = QMessageBox

    def getBool(self):
        self.input = self.message_box.question(
            self.parent, self.title, self.prompt, self.message_box.Yes | self.message_box.No)
        # Return True for yes and False for no
        return self.input == self.message_box.Yes

    def resetPreferences(self, file, menu=None, layout=None, reset_file=False):
        # Get input from user and continue only if input was 'yes'
        if self.getBool():
            if reset_file:
                JsonIO(file).copyFromBase()
            else:
                JsonIO(file).copyLayout(menu, layout)
            # Refresh menu button layout using JSON
            Globals.refreshMenus()
