from os import path


# Return path to stylesheet
def getPath(style):
    ui_path = path.dirname(__file__)
    styles_path = path.abspath(path.join(ui_path, 'styles'))
    final_path = path.abspath(path.join(styles_path, style))
    return final_path
