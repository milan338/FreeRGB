# check for updates on startup, setting to disable that
# scan for com ports, arduino gives back information such as number of strips, device name, local device name, other info?
# option to select com port, option to select led strip
# ensure QT assets referenced locally
# patreon / buy coffee in options
# debug menu / serial monitor -- only show if advanced mode selected in options -- also shows python print statements
# version button goes to github page
# make context menu invisible each time a button is pressed
# On startup get current colour, brightness etc from arduino and adjust values in app
# Loading bar

# PROVIDE OPEN-SOURCE LICENSE WITH ALL LICENSES
# CURRENT STUFF - TOGGLE SWITCH
#               - MATERIAL ICONS

# check for set colour to not reset colour i.e. check for if user actually selected a colour

# open file to write preferences in


# for each element in scrollview first add spacer then add new element
# Only open serial monitor if valid device is connect / selected
# store serial messages in array
# clear array whenever reload / clear output button


import sys

from ui.widgets.ToggleSwitch import ToggleSwitch

from ui.Ui_MainWindow import Ui_Form

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


class MainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # UI initialisation
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # Variable initialisation
        self.version_name = 'Version 0.1.0'
        self.current_context = None
        self.current_colour = None
        self.current_brightness = None
        # Setup UI elements
        self.setupButtons()
        self.colour_picker = QtWidgets.QColorDialog(self)
        self.ui.context_menus.hide()

    def mousePressEvent(self, event):
        self.handleButton()

    def setupButtons(self):
        # Bottom bar
        self.ui.btn_version.setText(self.version_name)
        self.ui.btn_effect_off.clicked.connect(self.toggleLeds)
        self.ui.btn_device_information.clicked.connect(
            lambda: QtWidgets.QMessageBox.information(self, 'Device Information', 'COM Port: \nStrips Connected: \nArduRGB Version: \nBoard: \nBaud Rate: '))
        self.ui.slider_brightness.sliderReleased.connect(self.getBright)

        # Left bar
        self.ui.btn_menu_effects.clicked.connect(
            lambda: self.changePage(self.ui.main_menus, 0))
        self.ui.btn_menu_settings.clicked.connect(
            lambda: self.changePage(self.ui.main_menus, 1))
        self.ui.btn_list_device.clicked.connect(
            lambda: self.changePage(self.ui.context_menus, 0, False))
        self.ui.btn_list_strip.clicked.connect(
            lambda: self.changePage(self.ui.context_menus, 1, False))

        # Effects menu
        self.ui.btn_effect_solid.clicked.connect(self.getColour)

        # Settings menu
        self.switch_advanced = ToggleSwitch()
        self.switch_updates = ToggleSwitch()
        self.ui.tmp_layout_settings_advanced.addWidget(self.switch_advanced)
        self.ui.tmp_layout_settings_updates.addWidget(self.switch_updates)
        self.switch_advanced.toggled.connect(
            lambda: print(self.switch_advanced))
        self.switch_updates.toggled.connect(
            lambda: print(self.switch_advanced))

    def handleButton(self):
        self.ui.context_menus.hide()
        self.current_context = None

    def handleSwitch(self):
        print('temp')

    def changePage(self, widget, index, hide_context=True):
        widget.setCurrentIndex(index)
        if hide_context:
            self.handleButton()
        else:
            if self.current_context == index:
                self.ui.context_menus.hide()
                self.current_context = None
            else:
                self.ui.context_menus.show()
                self.current_context = index

    def getColour(self):
        self.handleButton()
        self.colour_picker.exec()
        self.current_colour = self.colour_picker.currentColor().getRgb()
        print(self.current_colour)

    def getBright(self):
        self.handleButton()
        self.current_brightness = self.ui.slider_brightness.value()
        print(self.current_brightness)

    def toggleLeds(self, message):
        self.handleButton()
        print('serial sent')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.setWindowTitle('FreeRGB')
    # window.setWindowIcon()
    window.show()

    sys.exit(app.exec())
