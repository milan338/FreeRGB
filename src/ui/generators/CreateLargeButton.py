# This file is part of FreeRGB, an app to control lighting devices.
# Copyright (C) 2020 milan338.
#
# FreeRGB is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FreeRGB is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FreeRGB.  If not, see <https://www.gnu.org/licenses/>.

from src import Globals

from src.rw.JsonIO import JsonIO

from src.ui.ButtonActions import ButtonActions
from src.ui.widgets.HoverButton import HoverButton
from src.ui.widgets.ToggleSwitch import ToggleSwitch

from PyQt5.QtCore import Qt, QCoreApplication, QSize, QRect
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QWidget, QLayout, QHBoxLayout, QLabel


class CreateLargeButton():
    def __init__(self, vertical_element, spacer=False, effect_btn=False):
        self.vertical_element = vertical_element
        self.effect_btn = effect_btn
        # Add spacer between buttons
        if spacer:
            self.vertical_element.addItem(QSpacerItem(
                20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))
        self.translate = QCoreApplication.translate

    def createGenericButton(self, button_name, button_attributes, scroll_element, style, right_click_menu):
        # Get individual attributes
        self.command_type = button_attributes['command']['type']
        self.command_payload = button_attributes['command']['payload']
        # Initialise button
        self.btn = HoverButton(scroll_element)
        self.vertical_element.addWidget(self.btn)
        self.btn.setObjectName(button_name)
        self.btn.setText(self.translate("Form", button_attributes['text']))
        # Set size
        self.sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.btn.setSizePolicy(self.sizePolicy)
        self.btn.setMinimumSize(QSize(0, 100))
        self.btn.setMaximumSize(QSize(700, 100))
        # Create context menu
        self.btn.setContextMenuPolicy(Qt.CustomContextMenu)
        self.btn.customContextMenuRequested.connect(
            lambda: self.contextMenu(right_click_menu))
        # Set style
        self.btn.setProperty('style', style)
        # Set up hover detection
        self.btn.mouse_hovered.connect(self.setCurrentHoverButton)
        # Connect click action if button should run effect
        if self.effect_btn:
            self.btn.clicked.connect(lambda: self.runEffect(
                self.command_type, self.command_payload))
        # Connect click action if button should not run effect
        else:
            self.btn.clicked.connect(lambda: getattr(
                ButtonActions, self.command_type)(self.command_payload))
        # Show button
        self.btn.show()

    def createToggleButton(self, button_name, button_attributes, scroll_element, style):
        # Initialise button
        self.btn = QWidget(scroll_element)
        self.vertical_element.addWidget(self.btn)
        self.btn.setObjectName(button_name)
        # Set size
        self.sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.btn.setSizePolicy(self.sizePolicy)
        self.btn.setMinimumSize(QSize(0, 100))
        self.btn.setMaximumSize(QSize(700, 100))
        # Set style
        self.btn.setProperty('type', 'toggle-button')
        self.btn.setProperty('style', style)
        # Create horizontal layout for elements
        self.horizontal_layout_widget = QWidget(self.btn)
        self.horizontal_layout_widget.setGeometry(QRect(10, 3, 631, 102))
        self.horizontal_layout_widget.setObjectName(
            f'{button_name}_h_layout_widget')
        self.btn_layout = QHBoxLayout(self.horizontal_layout_widget)
        self.btn_layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.btn_layout.setContentsMargins(100, 0, 0, 0)
        self.btn_layout.setObjectName(f'{button_name}_layout')
        # Create spacer between text and switch
        self.spacer = QSpacerItem(
            100, 100, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.btn_layout.addItem(self.spacer)
        # Create toggle switch element
        self.switch = ToggleSwitch()
        self.switch.toggled.connect(lambda: self.updateBool(
            button_attributes['text'], button_name, self.switch))
        self.btn_layout.addWidget(self.switch)
        # Set toggle switch status
        if button_attributes['command']['payload']:
            self.switch.setChecked(True)
        # Add button label
        self.btn_label = QLabel(self.horizontal_layout_widget)
        self.btn_label.setMaximumSize(QSize(400, 100))
        self.btn_label.setObjectName(f'{button_name}_label')
        self.btn_label.setText(self.translate(
            "Form", button_attributes['text']))
        self.btn_layout.addWidget(self.btn_label)
        # Show button
        self.btn.show()

    def updateBool(self, text, entry_name, switch):
        # Update settings file
        JsonIO('settings.json').replaceEntry(entry_name, entry_name,
                                             text, 'toggleBool', switch.isChecked())
        # Run toggle action
        ButtonActions.toggleBool()

    def runEffect(self, effect, payload):
        try:
            # Import effect file
            self.module = __import__(
                f'{Globals.effect_import_path}.{effect}', fromlist=[None])
            # Create new effect instance
            self.effect_class = getattr(self.module, effect)
            self.effect_class(payload)
        except:
            pass

    def setCurrentHoverButton(self, hovered):
        if hovered:
            Globals.current_hovered_btn = self.btn
        else:
            pass

    def contextMenu(self, menu):
        menu.exec(QCursor.pos())
