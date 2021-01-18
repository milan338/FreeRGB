# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Milan\Documents\Software Projects\Python Projects\FreeRGB\src\ui\views\input\input_dialogue.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 250)
        Form.setMinimumSize(QtCore.QSize(400, 250))
        Form.setMaximumSize(QtCore.QSize(400, 250))
        Form.setStyleSheet("background-color: rgb(43, 47, 59);")
        self.input_effect_name = QtWidgets.QLineEdit(Form)
        self.input_effect_name.setGeometry(QtCore.QRect(10, 30, 381, 31))
        self.input_effect_name.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(51, 58, 72);\n"
"border-radius: 10px;")
        self.input_effect_name.setText("")
        self.input_effect_name.setObjectName("input_effect_name")
        self.input_effect_payload = QtWidgets.QLineEdit(Form)
        self.input_effect_payload.setGeometry(QtCore.QRect(10, 100, 381, 31))
        self.input_effect_payload.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(51, 58, 72);\n"
"border-radius: 10px;")
        self.input_effect_payload.setObjectName("input_effect_payload")
        self.btn_submit = QtWidgets.QPushButton(Form)
        self.btn_submit.setGeometry(QtCore.QRect(280, 210, 111, 31))
        self.btn_submit.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(39, 43, 54);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(51, 76, 100);\n"
"}\n"
"\n"
"QPushButton:pressed  {\n"
"    background-color: rgb(90, 164, 253);\n"
"}")
        self.btn_submit.setObjectName("btn_submit")
        self.label_effect_name = QtWidgets.QLabel(Form)
        self.label_effect_name.setGeometry(QtCore.QRect(20, 10, 81, 16))
        self.label_effect_name.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_effect_name.setObjectName("label_effect_name")
        self.label_effect_payload = QtWidgets.QLabel(Form)
        self.label_effect_payload.setGeometry(QtCore.QRect(20, 80, 81, 16))
        self.label_effect_payload.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_effect_payload.setObjectName("label_effect_payload")
        self.label_error = QtWidgets.QLabel(Form)
        self.label_error.setGeometry(QtCore.QRect(10, 220, 231, 20))
        self.label_error.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_error.setText("")
        self.label_error.setObjectName("label_error")
        self.btn_effect_types = QtWidgets.QPushButton(Form)
        self.btn_effect_types.setGeometry(QtCore.QRect(10, 170, 381, 31))
        self.btn_effect_types.setStyleSheet("QPushButton\n"
"{\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(51, 58, 72);\n"
"    border-radius: 10px;\n"
"     text-align: left;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"    background-color: rgb(51, 76, 100);\n"
"}\n"
"\n"
"QPushButton:pressed \n"
"{\n"
"    background-color: rgb(90, 164, 253);\n"
"}")
        self.btn_effect_types.setText("")
        self.btn_effect_types.setObjectName("btn_effect_types")
        self.label_effect_type = QtWidgets.QLabel(Form)
        self.label_effect_type.setGeometry(QtCore.QRect(20, 150, 81, 16))
        self.label_effect_type.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_effect_type.setObjectName("label_effect_type")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_submit.setText(_translate("Form", "Submit"))
        self.label_effect_name.setText(_translate("Form", "Effect Name"))
        self.label_effect_payload.setText(_translate("Form", "Effect Payload"))
        self.label_effect_type.setText(_translate("Form", "Effect Type"))