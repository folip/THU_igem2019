# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'encode.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EncodeWidget(object):
    def setupUi(self, EncodeWidget):
        EncodeWidget.setObjectName("EncodeWidget")
        EncodeWidget.resize(1265, 727)
        EncodeWidget.setAcceptDrops(True)
        EncodeWidget.setStyleSheet("background-color: rgb(34, 33, 33);")
        self.label_preview = QtWidgets.QLabel(EncodeWidget)
        self.label_preview.setGeometry(QtCore.QRect(40, 40, 526, 341))
        self.label_preview.setAcceptDrops(True)
        self.label_preview.setStyleSheet("font: 75 20pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.label_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.label_preview.setObjectName("label_preview")
        self.label_file_name = QtWidgets.QLabel(EncodeWidget)
        self.label_file_name.setGeometry(QtCore.QRect(40, 381, 526, 30))
        self.label_file_name.setAcceptDrops(True)
        self.label_file_name.setStyleSheet("font: 400 14pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.label_file_name.setText("")
        self.label_file_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_file_name.setObjectName("label_file_name")
        self.widget_size = QtWidgets.QWidget(EncodeWidget)
        self.widget_size.setGeometry(QtCore.QRect(40, 430, 526, 270))
        self.widget_size.setAcceptDrops(True)
        self.widget_size.setStyleSheet("background-color: rgb(50, 49, 49);")
        self.widget_size.setObjectName("widget_size")
        self.label_file_size = QtWidgets.QLabel(EncodeWidget)
        self.label_file_size.setGeometry(QtCore.QRect(92, 560, 211, 41))
        self.label_file_size.setAcceptDrops(True)
        self.label_file_size.setStyleSheet("font: 500 20pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: rgb(50, 49, 49);")
        self.label_file_size.setObjectName("label_file_size")
        self.label_chunk_num = QtWidgets.QLabel(EncodeWidget)
        self.label_chunk_num.setGeometry(QtCore.QRect(356, 560, 151, 41))
        self.label_chunk_num.setAcceptDrops(True)
        self.label_chunk_num.setStyleSheet("font: 500 20pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: rgb(50, 49, 49);")
        self.label_chunk_num.setObjectName("label_chunk_num")
        self.label_byte_5 = QtWidgets.QLabel(EncodeWidget)
        self.label_byte_5.setGeometry(QtCore.QRect(360, 640, 60, 4))
        self.label_byte_5.setAcceptDrops(True)
        self.label_byte_5.setStyleSheet("background-color: rgb(2, 154, 255);")
        self.label_byte_5.setText("")
        self.label_byte_5.setObjectName("label_byte_5")
        self.label_byte = QtWidgets.QLabel(EncodeWidget)
        self.label_byte.setGeometry(QtCore.QRect(95, 600, 211, 41))
        self.label_byte.setAcceptDrops(True)
        self.label_byte.setStyleSheet("font: 75 12pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: rgb(50, 49, 49);")
        self.label_byte.setObjectName("label_byte")
        self.label_byte_3 = QtWidgets.QLabel(EncodeWidget)
        self.label_byte_3.setGeometry(QtCore.QRect(359, 600, 171, 41))
        self.label_byte_3.setAcceptDrops(True)
        self.label_byte_3.setStyleSheet("font: 75 12pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: rgb(50, 49, 49);")
        self.label_byte_3.setObjectName("label_byte_3")
        self.label_byte_2 = QtWidgets.QLabel(EncodeWidget)
        self.label_byte_2.setGeometry(QtCore.QRect(96, 640, 60, 4))
        self.label_byte_2.setAcceptDrops(True)
        self.label_byte_2.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.label_byte_2.setText("")
        self.label_byte_2.setObjectName("label_byte_2")
        self.pushButton_icon_file = QtWidgets.QPushButton(EncodeWidget)
        self.pushButton_icon_file.setGeometry(QtCore.QRect(106, 470, 56, 56))
        self.pushButton_icon_file.setAcceptDrops(True)
        self.pushButton_icon_file.setStyleSheet("border: 0px;\n"
"background-color: rgb(50, 49, 49);")
        self.pushButton_icon_file.setText("")
        self.pushButton_icon_file.setObjectName("pushButton_icon_file")
        self.pushButton_icon_array = QtWidgets.QPushButton(EncodeWidget)
        self.pushButton_icon_array.setGeometry(QtCore.QRect(260, 470, 56, 56))
        self.pushButton_icon_array.setAcceptDrops(True)
        self.pushButton_icon_array.setStyleSheet("border: 0px;\n"
"background-color: rgb(50, 49, 49);")
        self.pushButton_icon_array.setText("")
        self.pushButton_icon_array.setObjectName("pushButton_icon_array")
        self.pushButton_icon_dna = QtWidgets.QPushButton(EncodeWidget)
        self.pushButton_icon_dna.setGeometry(QtCore.QRect(426, 470, 56, 56))
        self.pushButton_icon_dna.setAcceptDrops(True)
        self.pushButton_icon_dna.setStyleSheet("border: 0px;\n"
"background-color: rgb(50, 49, 49);")
        self.pushButton_icon_dna.setText("")
        self.pushButton_icon_dna.setObjectName("pushButton_icon_dna")
        self.label_homo_graph = QtWidgets.QLabel(EncodeWidget)
        self.label_homo_graph.setGeometry(QtCore.QRect(930, 70, 258, 194))
        self.label_homo_graph.setAcceptDrops(True)
        self.label_homo_graph.setStyleSheet("font: 75 20pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: rgb(50, 49, 49);\n"
"border: 2px solid white;")
        self.label_homo_graph.setText("")
        self.label_homo_graph.setObjectName("label_homo_graph")
        self.label_byte_6 = QtWidgets.QLabel(EncodeWidget)
        self.label_byte_6.setGeometry(QtCore.QRect(1040, 290, 61, 41))
        self.label_byte_6.setAcceptDrops(True)
        self.label_byte_6.setStyleSheet("font: 75 12pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: rgb(50, 49, 49);")
        self.label_byte_6.setObjectName("label_byte_6")
        self.label_homo_chunks = QtWidgets.QLabel(EncodeWidget)
        self.label_homo_chunks.setGeometry(QtCore.QRect(930, 290, 111, 41))
        self.label_homo_chunks.setAcceptDrops(True)
        self.label_homo_chunks.setStyleSheet("font: 500 20pt \"Segoe UI\";\n"
"color: red;\n"
"background-color: rgb(50, 49, 49);")
        self.label_homo_chunks.setObjectName("label_homo_chunks")
        self.label_byte_8 = QtWidgets.QLabel(EncodeWidget)
        self.label_byte_8.setGeometry(QtCore.QRect(930, 330, 171, 41))
        self.label_byte_8.setAcceptDrops(True)
        self.label_byte_8.setStyleSheet("font: 500 12pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: rgb(50, 49, 49);")
        self.label_byte_8.setObjectName("label_byte_8")
        self.widget_chunks = QtWidgets.QWidget(EncodeWidget)
        self.widget_chunks.setGeometry(QtCore.QRect(610, 30, 611, 391))
        self.widget_chunks.setAcceptDrops(True)
        self.widget_chunks.setStyleSheet("background-color: rgb(50, 49, 49);")
        self.widget_chunks.setObjectName("widget_chunks")
        self.widget_config = QtWidgets.QWidget(EncodeWidget)
        self.widget_config.setGeometry(QtCore.QRect(610, 460, 611, 141))
        self.widget_config.setAcceptDrops(True)
        self.widget_config.setStyleSheet("background-color: rgb(50, 49, 49);")
        self.widget_config.setObjectName("widget_config")
        self.label_byte_9 = QtWidgets.QLabel(self.widget_config)
        self.label_byte_9.setGeometry(QtCore.QRect(30, 50, 171, 41))
        self.label_byte_9.setAcceptDrops(True)
        self.label_byte_9.setStyleSheet("font: 500 20pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: rgb(50, 49, 49);")
        self.label_byte_9.setObjectName("label_byte_9")
        self.pushButton_start = QtWidgets.QPushButton(EncodeWidget)
        self.pushButton_start.setGeometry(QtCore.QRect(610, 635, 611, 61))
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
        self.pushButton_icon_fountain = QtWidgets.QPushButton(EncodeWidget)
        self.pushButton_icon_fountain.setGeometry(QtCore.QRect(880, 500, 56, 56))
        self.pushButton_icon_fountain.setAcceptDrops(True)
        self.pushButton_icon_fountain.setStyleSheet("QPushButton#pushButton_icon_fountain{\n"
"border: 0px;\n"
"background-color: rgb(50, 49, 49);\n"
"}\n"
"QPushButton#pushButton_icon_fountain:hover{\n"
"border: 1px solid rgb(255, 170, 0);\n"
"background-color: rgb(50, 49, 49);\n"
"}\n"
"")
        self.pushButton_icon_fountain.setText("")
        self.pushButton_icon_fountain.setObjectName("pushButton_icon_fountain")
        self.pushButton_icon_mask = QtWidgets.QPushButton(EncodeWidget)
        self.pushButton_icon_mask.setGeometry(QtCore.QRect(1040, 500, 56, 56))
        self.pushButton_icon_mask.setAcceptDrops(True)
        self.pushButton_icon_mask.setStyleSheet("QPushButton#pushButton_icon_mask{\n"
"border: 0px;\n"
"background-color: rgb(50, 49, 49);\n"
"}\n"
"QPushButton#pushButton_icon_mask:hover{\n"
"border: 1px solid rgb(255, 170, 0);\n"
"background-color: rgb(50, 49, 49);\n"
"}\n"
"")
        self.pushButton_icon_mask.setText("")
        self.pushButton_icon_mask.setObjectName("pushButton_icon_mask")
        self.label_file_alarm = QtWidgets.QLabel(EncodeWidget)
        self.label_file_alarm.setGeometry(QtCore.QRect(462, 320, 340, 60))
        self.label_file_alarm.setStyleSheet("border-radius:8px;\n"
"border: 3px solid rgb(230, 60, 60);\n"
"background-color: rgb(180, 30, 30);\n"
"font: 400 18pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.label_file_alarm.setAlignment(QtCore.Qt.AlignCenter)
        self.label_file_alarm.setObjectName("label_file_alarm")
        self.label_CG_graph = QtWidgets.QLabel(EncodeWidget)
        self.label_CG_graph.setGeometry(QtCore.QRect(650, 70, 258, 194))
        self.label_CG_graph.setAcceptDrops(True)
        self.label_CG_graph.setStyleSheet("font: 75 20pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: rgb(50, 49, 49);\n"
"border: 2px solid white;")
        self.label_CG_graph.setText("")
        self.label_CG_graph.setObjectName("label_CG_graph")
        self.label_byte_7 = QtWidgets.QLabel(EncodeWidget)
        self.label_byte_7.setGeometry(QtCore.QRect(650, 330, 171, 41))
        self.label_byte_7.setAcceptDrops(True)
        self.label_byte_7.setStyleSheet("font: 500 12pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: rgb(50, 49, 49);")
        self.label_byte_7.setObjectName("label_byte_7")
        self.label_CG_chunks = QtWidgets.QLabel(EncodeWidget)
        self.label_CG_chunks.setGeometry(QtCore.QRect(650, 290, 111, 41))
        self.label_CG_chunks.setAcceptDrops(True)
        self.label_CG_chunks.setStyleSheet("font: 500 20pt \"Segoe UI\";\n"
"color: red;\n"
"background-color: rgb(50, 49, 49);")
        self.label_CG_chunks.setObjectName("label_CG_chunks")
        self.label_byte_4 = QtWidgets.QLabel(EncodeWidget)
        self.label_byte_4.setGeometry(QtCore.QRect(760, 290, 61, 41))
        self.label_byte_4.setAcceptDrops(True)
        self.label_byte_4.setStyleSheet("font: 75 12pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: rgb(50, 49, 49);")
        self.label_byte_4.setObjectName("label_byte_4")
        self.label_loading_text = QtWidgets.QLabel(EncodeWidget)
        self.label_loading_text.setGeometry(QtCore.QRect(420, 330, 171, 41))
        self.label_loading_text.setAcceptDrops(True)
        self.label_loading_text.setStyleSheet("font: 500 20pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: rgb(50, 49, 49);")
        self.label_loading_text.setObjectName("label_loading_text")
        self.label_loading_background = QtWidgets.QLabel(EncodeWidget)
        self.label_loading_background.setGeometry(QtCore.QRect(330, 310, 601, 91))
        self.label_loading_background.setAcceptDrops(True)
        self.label_loading_background.setStyleSheet("background-color: rgb(50, 49, 49);")
        self.label_loading_background.setText("")
        self.label_loading_background.setObjectName("label_loading_background")
        self.pushButton_loading_icon = QtWidgets.QPushButton(EncodeWidget)
        self.pushButton_loading_icon.setGeometry(QtCore.QRect(710, 330, 56, 56))
        self.pushButton_loading_icon.setAcceptDrops(True)
        self.pushButton_loading_icon.setStyleSheet("border: 0px;\n"
"background-color: rgb(50, 49, 49);")
        self.pushButton_loading_icon.setText("")
        self.pushButton_loading_icon.setObjectName("pushButton_loading_icon")
        self.widget_chunks.raise_()
        self.label_preview.raise_()
        self.label_file_name.raise_()
        self.widget_size.raise_()
        self.label_file_size.raise_()
        self.label_chunk_num.raise_()
        self.label_byte_5.raise_()
        self.label_byte.raise_()
        self.label_byte_3.raise_()
        self.label_byte_2.raise_()
        self.pushButton_icon_file.raise_()
        self.pushButton_icon_array.raise_()
        self.pushButton_icon_dna.raise_()
        self.label_homo_graph.raise_()
        self.label_byte_6.raise_()
        self.label_homo_chunks.raise_()
        self.label_byte_8.raise_()
        self.widget_config.raise_()
        self.pushButton_start.raise_()
        self.pushButton_icon_fountain.raise_()
        self.pushButton_icon_mask.raise_()
        self.label_CG_graph.raise_()
        self.label_byte_7.raise_()
        self.label_CG_chunks.raise_()
        self.label_byte_4.raise_()
        self.label_file_alarm.raise_()
        self.label_loading_background.raise_()
        self.label_loading_text.raise_()
        self.pushButton_loading_icon.raise_()

        self.retranslateUi(EncodeWidget)
        QtCore.QMetaObject.connectSlotsByName(EncodeWidget)

    def retranslateUi(self, EncodeWidget):
        _translate = QtCore.QCoreApplication.translate
        EncodeWidget.setWindowTitle(_translate("EncodeWidget", "Form"))
        self.label_preview.setText(_translate("EncodeWidget", "Drag File to Here"))
        self.label_file_size.setText(_translate("EncodeWidget", "0"))
        self.label_chunk_num.setText(_translate("EncodeWidget", "0"))
        self.label_byte.setText(_translate("EncodeWidget", "bytes"))
        self.label_byte_3.setText(_translate("EncodeWidget", "DNA chunks"))
        self.label_byte_6.setText(_translate("EncodeWidget", "chunks"))
        self.label_homo_chunks.setText(_translate("EncodeWidget", "0"))
        self.label_byte_8.setText(_translate("EncodeWidget", "with long homo"))
        self.label_byte_9.setText(_translate("EncodeWidget", "Encoding"))
        self.pushButton_start.setText(_translate("EncodeWidget", "start encoding"))
        self.label_file_alarm.setText(_translate("EncodeWidget", "Please Import Your File"))
        self.label_byte_7.setText(_translate("EncodeWidget", "GC out of range"))
        self.label_CG_chunks.setText(_translate("EncodeWidget", "0"))
        self.label_byte_4.setText(_translate("EncodeWidget", "chunks"))
        self.label_loading_text.setText(_translate("EncodeWidget", "Encoding..."))
