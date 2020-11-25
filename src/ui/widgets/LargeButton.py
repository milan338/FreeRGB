from PyQt5 import QtCore
from PyQt5 import QtWidgets


class CreateLargeButton():
    def __init__(self, vertical_element, spacer=False):
        self.vertical_element = vertical_element
        # Add spacer between buttons
        if spacer:
            self.vertical_element.addItem(QtWidgets.QSpacerItem(
                20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed))
        self.translate = QtCore.QCoreApplication.translate

    def createGenericButton(self, text, obj_name, scroll_element, style_sheet):
        self.btn = QtWidgets.QPushButton(scroll_element)
        self.vertical_element.addWidget(self.btn)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.btn.setSizePolicy(sizePolicy)
        self.btn.setMinimumSize(QtCore.QSize(0, 100))
        self.btn.setMaximumSize(QtCore.QSize(700, 100))
        with open(style_sheet) as style_file:
            self.btn.setStyleSheet(style_file.read())
        self.btn.setObjectName(obj_name)
        self.btn.setText(self.translate("Form", text))
        self.btn.show()
