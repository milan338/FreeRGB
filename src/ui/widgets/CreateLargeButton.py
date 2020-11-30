# from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QCoreApplication, QSize
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QPushButton


class CreateLargeButton():
    def __init__(self, vertical_element, spacer=False):
        self.vertical_element = vertical_element
        # Add spacer between buttons
        if spacer:
            self.vertical_element.addItem(QSpacerItem(
                20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))
        self.translate = QCoreApplication.translate

    def createGenericButton(self, text, obj_name, scroll_element, style_sheet, right_click_menu):
        # Initialise button
        self.btn = QPushButton(scroll_element)
        self.vertical_element.addWidget(self.btn)
        self.btn.setObjectName(obj_name)
        self.btn.setText(self.translate("Form", text))
        # Set size
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.btn.setSizePolicy(sizePolicy)
        self.btn.setMinimumSize(QSize(0, 100))
        self.btn.setMaximumSize(QSize(700, 100))
        # Create context menu
        self.btn.setContextMenuPolicy(Qt.CustomContextMenu)
        self.btn.customContextMenuRequested.connect(
            lambda: self.contextMenu(right_click_menu))
        # Set style
        with open(style_sheet) as style_file:
            self.btn.setStyleSheet(style_file.read())
        # Show button
        self.btn.show()

    def contextMenu(self, menu):
        menu.exec(QCursor.pos())
