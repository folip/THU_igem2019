# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HomeWidget(object):
    def setupUi(self, HomeWidget):
        HomeWidget.setObjectName("HomeWidget")
        HomeWidget.resize(1265, 727)
        HomeWidget.setStyleSheet("background-color: rgb(34, 33, 33);")
        self.button_encode = QtWidgets.QPushButton(HomeWidget)
        self.button_encode.setGeometry(QtCore.QRect(150, 91, 427, 546))
        self.button_encode.setStyleSheet("QPushButton#button_encode{\n"
"border: 0px;\n"
"}\n"
"QPushButton#button_encode:hover{\n"
"border: 2px solid rgb(0, 89, 136);\n"
"}\n"
"")
        self.button_encode.setText("")
        self.button_encode.setObjectName("button_encode")
        self.button_decode = QtWidgets.QPushButton(HomeWidget)
        self.button_decode.setGeometry(QtCore.QRect(690, 91, 427, 546))
        self.button_decode.setStyleSheet("QPushButton#button_decode{\n"
"border: 0px;\n"
"}\n"
"QPushButton#button_decode:hover{\n"
"border: 2px solid rgb(0, 89, 136);\n"
"}\n"
"")
        self.button_decode.setText("")
        self.button_decode.setObjectName("button_decode")

        self.retranslateUi(HomeWidget)
        QtCore.QMetaObject.connectSlotsByName(HomeWidget)

    def retranslateUi(self, HomeWidget):
        _translate = QtCore.QCoreApplication.translate
        HomeWidget.setWindowTitle(_translate("HomeWidget", "Form"))
