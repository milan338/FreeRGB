from os import path

from ui.GenerateButtons import GenerateButtons
from ui.Ui_MainWindow import Ui_Form

# Return path to stylesheet


def getPath(style):
    ui_path = path.dirname(__file__)
    styles_path = path.abspath(path.join(ui_path, 'styles'))
    final_path = path.abspath(path.join(styles_path, style))
    return final_path
