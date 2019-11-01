# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progress_bar.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(611, 101)
        Dialog.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(240, 10, 171, 41))
        self.label.setAcceptDrops(True)
        self.label.setStyleSheet("font: 500 20pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: rgb(50, 49, 49);")
        self.label.setObjectName("label")
        self.label_background = QtWidgets.QLabel(Dialog)
        self.label_background.setGeometry(QtCore.QRect(5, 5, 601, 91))
        self.label_background.setAcceptDrops(True)
        self.label_background.setStyleSheet("background-color: rgb(50, 49, 49);")
        self.label_background.setText("")
        self.label_background.setObjectName("label_background")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(30, 70, 561, 5))
        self.progressBar.setStyleSheet("QProgressBar#progressBar{\n"
"color: rgb(255, 0, 0);\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:5px;\n"
"border: 0;}\n"
"QProgressBar#progressBar:chunk{\n"
"background-color: rgb(255, 0, 0);\n"
"border-radius:5px;\n"
"}")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.label_background.raise_()
        self.label.raise_()
        self.progressBar.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Encoding..."))
