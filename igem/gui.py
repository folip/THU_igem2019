# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UI_Main(object):
    def setupUi(self, UI_Main):
        UI_Main.setObjectName("UI_Main")
        UI_Main.setWindowModality(QtCore.Qt.NonModal)
        UI_Main.resize(1376, 778)
        UI_Main.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(UI_Main)
        self.centralwidget.setObjectName("centralwidget")
        self.button_home = QtWidgets.QPushButton(self.centralwidget)
        self.button_home.setGeometry(QtCore.QRect(5, 135, 91, 81))
        self.button_home.setStyleSheet("QPushButton#button_home{\n"
"border:0px;\n"
"background-color: rgb(13, 12, 12);\n"
"color: rgb(255, 255, 255)}\n"
"QPushButton#button_home:hover{\n"
"border:0px;\n"
"background-color: rgb(30, 29, 29);\n"
"color: rgb(255, 255, 255)}\n"
"")
        self.button_home.setText("")
        self.button_home.setObjectName("button_home")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(100, 46, 1265, 727))
        self.frame.setStyleSheet("background-color: rgb(34, 33, 33);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.button_close = QtWidgets.QPushButton(self.centralwidget)
        self.button_close.setGeometry(QtCore.QRect(1300, 5, 66, 41))
        self.button_close.setStyleSheet("QPushButton#button_close{\n"
"border: 0px;\n"
"font: 75 11pt \"Adobe Gothic Std B\";\n"
"background-color: rgb(34, 33, 33);\n"
"color: rgb(255, 255, 255)}\n"
"QPushButton#button_close:hover{\n"
"border: 0px;\n"
"font: 75 11pt \"Adobe Gothic Std B\";\n"
"background-color: rgb(255, 0, 0);\n"
"color: rgb(255, 255, 255)}\n"
"")
        self.button_close.setText("")
        self.button_close.setObjectName("button_close")
        self.button_page1 = QtWidgets.QPushButton(self.centralwidget)
        self.button_page1.setGeometry(QtCore.QRect(5, 235, 91, 81))
        self.button_page1.setStyleSheet("QPushButton#button_page1{\n"
"border:0px;\n"
"background-color: rgb(50, 49, 49);\n"
"color: rgb(255, 255, 255)}\n"
"QPushButton#button_page1:hover{\n"
"border:0px;\n"
"background-color: rgb(30, 29, 29);\n"
"color: rgb(255, 255, 255)}\n"
"")
        self.button_page1.setText("")
        self.button_page1.setObjectName("button_page1")
        self.label_paint = QtWidgets.QLabel(self.centralwidget)
        self.label_paint.setGeometry(QtCore.QRect(5, 5, 91, 768))
        self.label_paint.setStyleSheet("background-color: rgb(50, 49, 49);")
        self.label_paint.setText("")
        self.label_paint.setObjectName("label_paint")
        self.label_home = QtWidgets.QLabel(self.centralwidget)
        self.label_home.setGeometry(QtCore.QRect(7, 145, 5, 61))
        self.label_home.setStyleSheet("background-color: rgb(245, 92, 61);")
        self.label_home.setText("")
        self.label_home.setObjectName("label_home")
        self.label_page1 = QtWidgets.QLabel(self.centralwidget)
        self.label_page1.setGeometry(QtCore.QRect(7, 245, 5, 61))
        self.label_page1.setStyleSheet("background-color: rgb(245, 92, 61);")
        self.label_page1.setText("")
        self.label_page1.setObjectName("label_page1")
        self.button_mini = QtWidgets.QPushButton(self.centralwidget)
        self.button_mini.setGeometry(QtCore.QRect(1234, 5, 66, 41))
        self.button_mini.setStyleSheet("QPushButton#button_mini{\n"
"border: 0px;\n"
"font: 75 11pt \"Adobe Gothic Std B\";\n"
"background-color: rgb(34, 33, 33);\n"
"color: rgb(255, 255, 255)}\n"
"QPushButton#button_mini:hover{\n"
"border: 0px;\n"
"font: 75 11pt \"Adobe Gothic Std B\";\n"
"background-color: rgb(255, 0, 0);\n"
"color: rgb(255, 255, 255)}\n"
"")
        self.button_mini.setText("")
        self.button_mini.setObjectName("button_mini")
        self.label_background = QtWidgets.QLabel(self.centralwidget)
        self.label_background.setGeometry(QtCore.QRect(5, 5, 1366, 768))
        self.label_background.setStyleSheet("background-color: rgb(34, 33, 33);")
        self.label_background.setText("")
        self.label_background.setObjectName("label_background")
        self.button_page2 = QtWidgets.QPushButton(self.centralwidget)
        self.button_page2.setGeometry(QtCore.QRect(5, 335, 91, 81))
        self.button_page2.setStyleSheet("QPushButton#button_page2{\n"
"border:0px;\n"
"background-color: rgb(50, 49, 49);\n"
"color: rgb(255, 255, 255)}\n"
"QPushButton#button_page2:hover{\n"
"border:0px;\n"
"background-color: rgb(30, 29, 29);\n"
"color: rgb(255, 255, 255)}\n"
"")
        self.button_page2.setText("")
        self.button_page2.setObjectName("button_page2")
        self.label_page2 = QtWidgets.QLabel(self.centralwidget)
        self.label_page2.setGeometry(QtCore.QRect(7, 345, 5, 61))
        self.label_page2.setStyleSheet("background-color: rgb(245, 92, 61);")
        self.label_page2.setText("")
        self.label_page2.setObjectName("label_page2")
        self.label_background.raise_()
        self.frame.raise_()
        self.button_close.raise_()
        self.label_paint.raise_()
        self.button_home.raise_()
        self.button_page1.raise_()
        self.label_home.raise_()
        self.label_page1.raise_()
        self.button_mini.raise_()
        self.button_page2.raise_()
        self.label_page2.raise_()
        UI_Main.setCentralWidget(self.centralwidget)

        self.retranslateUi(UI_Main)
        QtCore.QMetaObject.connectSlotsByName(UI_Main)

    def retranslateUi(self, UI_Main):
        _translate = QtCore.QCoreApplication.translate
        UI_Main.setWindowTitle(_translate("UI_Main", "MainWindow"))
