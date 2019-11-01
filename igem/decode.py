# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'decode.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DecodeWidget(object):
    def setupUi(self, DecodeWidget):
        DecodeWidget.setObjectName("DecodeWidget")
        DecodeWidget.resize(1265, 727)
        DecodeWidget.setAcceptDrops(True)
        DecodeWidget.setStyleSheet("background-color: rgb(34, 33, 33);")
        self.label_preview = QtWidgets.QLabel(DecodeWidget)
        self.label_preview.setGeometry(QtCore.QRect(340, 100, 571, 391))
        self.label_preview.setAcceptDrops(True)
        self.label_preview.setStyleSheet("font: 75 20pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.label_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.label_preview.setObjectName("label_preview")
        self.pushButton_start = QtWidgets.QPushButton(DecodeWidget)
        self.pushButton_start.setGeometry(QtCore.QRect(330, 560, 611, 61))
        self.pushButton_start.setAcceptDrops(True)
        self.pushButton_start.setStyleSheet("QPushButton#pushButton_start{\n"
"border: 0px;\n"
"background-color: rgb(240, 20, 20);\n"
"font: 500 20pt \"Segoe UI\";\n"
"color: white;}\n"
"QPushButton#pushButton_start:pressed{\n"
"border: 0px;\n"
"background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.24 rgba(240, 20, 20, 180), stop:0.52 rgba(240, 20, 20, 210), stop:1 rgba(240, 20, 20, 240));\n"
"font: 500 20pt \"Segoe UI\";\n"
"color: white;}")
        self.pushButton_start.setObjectName("pushButton_start")
        self.label_file_name = QtWidgets.QLabel(DecodeWidget)
        self.label_file_name.setGeometry(QtCore.QRect(360, 500, 526, 30))
        self.label_file_name.setAcceptDrops(True)
        self.label_file_name.setStyleSheet("font: 400 14pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.label_file_name.setText("")
        self.label_file_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_file_name.setObjectName("label_file_name")
        self.label_file_alarm = QtWidgets.QLabel(DecodeWidget)
        self.label_file_alarm.setGeometry(QtCore.QRect(462, 320, 340, 60))
        self.label_file_alarm.setStyleSheet("border-radius:8px;\n"
"border: 3px solid rgb(230, 60, 60);\n"
"background-color: rgb(180, 30, 30);\n"
"font: 400 18pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.label_file_alarm.setAlignment(QtCore.Qt.AlignCenter)
        self.label_file_alarm.setObjectName("label_file_alarm")
        self.pushButton_loading_icon = QtWidgets.QPushButton(DecodeWidget)
        self.pushButton_loading_icon.setGeometry(QtCore.QRect(700, 340, 56, 56))
        self.pushButton_loading_icon.setAcceptDrops(True)
        self.pushButton_loading_icon.setStyleSheet("border: 0px;\n"
"background-color: rgb(50, 49, 49);")
        self.pushButton_loading_icon.setText("")
        self.pushButton_loading_icon.setObjectName("pushButton_loading_icon")
        self.label_loading_background = QtWidgets.QLabel(DecodeWidget)
        self.label_loading_background.setGeometry(QtCore.QRect(325, 320, 601, 91))
        self.label_loading_background.setAcceptDrops(True)
        self.label_loading_background.setStyleSheet("background-color: rgb(50, 49, 49);")
        self.label_loading_background.setText("")
        self.label_loading_background.setObjectName("label_loading_background")
        self.label_loading_text = QtWidgets.QLabel(DecodeWidget)
        self.label_loading_text.setGeometry(QtCore.QRect(415, 340, 171, 41))
        self.label_loading_text.setAcceptDrops(True)
        self.label_loading_text.setStyleSheet("font: 500 20pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: rgb(50, 49, 49);")
        self.label_loading_text.setObjectName("label_loading_text")
        self.label_preview.raise_()
        self.pushButton_start.raise_()
        self.label_file_name.raise_()
        self.label_file_alarm.raise_()
        self.label_loading_background.raise_()
        self.pushButton_loading_icon.raise_()
        self.label_loading_text.raise_()

        self.retranslateUi(DecodeWidget)
        QtCore.QMetaObject.connectSlotsByName(DecodeWidget)

    def retranslateUi(self, DecodeWidget):
        _translate = QtCore.QCoreApplication.translate
        DecodeWidget.setWindowTitle(_translate("DecodeWidget", "Form"))
        self.label_preview.setText(_translate("DecodeWidget", "Drag File Here"))
        self.pushButton_start.setText(_translate("DecodeWidget", "start decoding"))
        self.label_file_alarm.setText(_translate("DecodeWidget", "Please Import Your File"))
        self.label_loading_text.setText(_translate("DecodeWidget", "Encoding..."))
