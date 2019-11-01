# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CodingConfigDialog(object):
    def setupUi(self, CodingConfigDialog):
        CodingConfigDialog.setObjectName("CodingConfigDialog")
        CodingConfigDialog.resize(508, 610)
        CodingConfigDialog.setStyleSheet("background-color: rgba(34, 33, 33, 0);")
        self.label = QtWidgets.QLabel(CodingConfigDialog)
        self.label.setGeometry(QtCore.QRect(35, 25, 441, 51))
        self.label.setStyleSheet("font: 75 20pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton_ok = QtWidgets.QPushButton(CodingConfigDialog)
        self.pushButton_ok.setGeometry(QtCore.QRect(35, 535, 201, 41))
        self.pushButton_ok.setStyleSheet("border-radius:8px;\n"
"border: 0px;\n"
"background-color: rgb(220, 70, 70);\n"
"font: 400 12pt \"Segoe UI\";")
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.pushButton_cancel = QtWidgets.QPushButton(CodingConfigDialog)
        self.pushButton_cancel.setGeometry(QtCore.QRect(275, 535, 201, 41))
        self.pushButton_cancel.setStyleSheet("border-radius:8px;\n"
"border: 0px;\n"
"background-color: rgb(175, 175, 175);\n"
"font: 400 12pt \"Segoe UI\";")
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.textEdit = QtWidgets.QTextEdit(CodingConfigDialog)
        self.textEdit.setGeometry(QtCore.QRect(25, 110, 456, 401))
        self.textEdit.setStyleSheet("QTextEdit#textEdit{\n"
"border-radius:8px;\n"
"border: 1px solid white;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 10pt \"Segoe UI\";}\n"
"QTextEdit#textEdit:hover{\n"
"border-radius:8px;\n"
"border: 2px solid white;\n"
"background-color: rgb(51, 50, 50);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 10pt \"Segoe UI\";}\n"
"\n"
"\n"
"")
        self.textEdit.setObjectName("textEdit")
        self.label_background = QtWidgets.QLabel(CodingConfigDialog)
        self.label_background.setGeometry(QtCore.QRect(5, 5, 498, 600))
        self.label_background.setStyleSheet("background-color: rgb(34, 33, 33);")
        self.label_background.setText("")
        self.label_background.setObjectName("label_background")
        self.label_background.raise_()
        self.label.raise_()
        self.pushButton_ok.raise_()
        self.pushButton_cancel.raise_()
        self.textEdit.raise_()

        self.retranslateUi(CodingConfigDialog)
        QtCore.QMetaObject.connectSlotsByName(CodingConfigDialog)

    def retranslateUi(self, CodingConfigDialog):
        _translate = QtCore.QCoreApplication.translate
        CodingConfigDialog.setWindowTitle(_translate("CodingConfigDialog", "Dialog"))
        self.label.setText(_translate("CodingConfigDialog", "Fountain Config"))
        self.pushButton_ok.setText(_translate("CodingConfigDialog", "OK"))
        self.pushButton_cancel.setText(_translate("CodingConfigDialog", "CANCEL"))
