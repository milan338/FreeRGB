import Globals


class SolidColour():
    def __init__(self):
        self.getColour()

    def getColour(self):
        self.handleButton()
        Globals.colour_picker.exec()
        self.current_colour = self.colour_picker.currentColor().getRgb()
        print(self.current_colour)

    @staticmethod
    def effectData():
        effect_name = 'Solid Colour'
        return effect_name
