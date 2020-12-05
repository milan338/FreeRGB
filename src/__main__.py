# check for updates on startup, setting to disable that
# scan for com ports, arduino gives back information such as number of strips, device name, local device name, other info?
# option to select com port, option to select led strip
# debug menu / serial monitor -- only show if advanced mode selected in options -- also shows python print statements
# version button goes to github page
# On startup get current colour, brightness etc from arduino and adjust values in app
# Loading bar

# PROVIDE OPEN-SOURCE LICENSE WITH ALL LICENSES
# CURRENT STUFF - TOGGLE SWITCH
#               - MATERIAL ICONS

# check for set colour to not reset colour i.e. check for if user actually selected a colour

# Only open serial monitor if valid device is connect / selected
# store serial messages in array
# clear array whenever reload / clear output button

# Button to reset settings

# Attach scrollbar on side of menu to scroll the main window

# implement logging system

# Get designer using stylesheets from external files

# Edit button in right click

import sys

import Globals

from rw.JsonIO import JsonIO

from ui import getPath
from ui.GenerateButtons import GenerateButtons
from ui.views.monitor.SerialMonitor import SerialMonitor
from ui.views.input.InputDialogue import InputDialogue
from ui.widgets.ToggleSwitch import ToggleSwitch
from ui.generators.CreateLargeButton import CreateLargeButton
from ui.generators.CreateMenuRC import CreateMenuRC
from ui.generators.CreateMessageBox import CreateMessageBox
from ui.views.main.Ui_MainWindow import Ui_Form

from PyQt5.QtWidgets import QWidget, QColorDialog, QMessageBox, QApplication
from PyQt5 import QtCore
from PyQt5 import QtGui


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Allow global access to refresh main menu using JSON
        Globals.refreshMenus = lambda: self.refreshMenus()
        # Initialise settings
        self.setupFiles()
        # UI initialisation
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # Variable initialisation
        self.version_name = JsonIO('app_Version.json').readEntry('version')
        self.current_context = None
        self.current_colour = None
        self.current_brightness = None
        # Setup UI elements
        self.setRightClickMenu()
        self.setupButtons()
        self.colour_picker = QColorDialog(self)
        self.ui.context_menus.hide()

    def setupFiles(self):
        self.init_files = ['menus.json', 'preferences.json']
        # Copy all files from base dir if they don't already exist
        for file in self.init_files:
            if JsonIO(file).fileExists():
                pass
            else:
                JsonIO(file).copyFromBase()

    def refreshMenus(self):
        GenerateButtons('menus.json', 'main_menu').removeButtons(
            self.ui.main_menu_button_layout)
        GenerateButtons('menus.json', 'main_menu').generateGenericButtons(self.ui.main_menu_button_layout, self.ui.effects_scroll_region, getPath(
            'button_generic_primary.qss'), self.right_click_menu_effects, spacer=True)

    def setupButtons(self):
        self.refreshMenus()

        # Bottom bar
        self.ui.btn_version.setText(self.version_name)
        self.ui.btn_device_debug.clicked.connect(
            lambda: self.initSerialMonitor())
        self.ui.btn_effect_off.clicked.connect(self.toggleLeds)
        self.ui.btn_device_information.clicked.connect(
            lambda: QMessageBox.information(self, 'Device Information', 'Device Name: \nCOM Port: \nStrips Connected: \nArduRGB Version: \nBoard: \nBaud Rate: '))
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
        # self.ui.btn_effect_solid.clicked.connect(self.getColour)
        # self.ui.btn_effect_solid.clicked.connect(
        #     lambda: JsonIO('preferences.json').writeEntry('advanced_mode'))
        # self.ui.btn_menu_effect_new.clicked.connect(
        #     lambda: self.addButton(self.ui.main_menu_button_layout))

        self.ui.btn_menu_effect_new.clicked.connect(lambda: self.initDialogue(
            'serial_direct', 'main_menu', 'Create New Effect'))
        self.ui.btn_menu_effect_reset.clicked.connect(lambda: CreateMessageBox(
            'Reset Effects Menu', 'This action will erase all custom effects you have specified. Continue?').resetPreferences(
            file='menus.json', menu='main_menu', layout='main_menu_button_layout'))

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

    def setRightClickMenu(self):
        # Read entries from JSON
        self.right_click_menu_effects_options = JsonIO(
            'right_click_menu.json').readEntry('main_menu_right_click_menu')
        # Create new right click menu
        self.right_click_menu_effects = CreateMenuRC(
            parent=self).makeMenu(getPath('right_click_menu.qss'))
        # Add all JSON entries as options to right click menu
        for entry_name, entry_payload in self.right_click_menu_effects_options.items():
            CreateMenuRC(parent=self).addOption(
                self.right_click_menu_effects, entry_name, entry_payload)

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

    def setWindowParams(self, window, title, icon=None):
        self.handleButton()
        window.show()
        window.setWindowTitle(title)
        # window.setWindowIcon(icon)

    def initSerialMonitor(self):
        self.serial_monitor = SerialMonitor()
        self.setWindowParams(self.serial_monitor, 'ArduRGB Debug View')

    def initDialogue(self, input_type, menu, window_title):
        self.input_dialogue = InputDialogue(
            input_type, menu, lambda: self.refreshMenus())
        self.setWindowParams(self.input_dialogue, window_title)

    def mousePressEvent(self, event):
        self.handleButton()

    def addButton(self, vertical_layout):
        # CreateLargeButton('text' + str(self.x), 'object', False, self.ui.effects_scroll_region,
        #                   self.ui.verticalLayout_2, getPath('button_generic_primary.qss'))
        # CreateLargeButton(vertical_layout, spacer=True).createGenericButton(
        #     'text' + str(self.x), 'object', self.ui.effects_scroll_region, getPath('button_generic_primary.qss'))
        GenerateButtons('menus.json', 'main_menu').generateGenericButtons(
            vertical_layout, self.ui.effects_scroll_region, getPath('button_generic_primary.qss'), spacer=True)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setWindowTitle('title')
    # window.setWindowIcon()
    window.show()

    sys.exit(app.exec_())
