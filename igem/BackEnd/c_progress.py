import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtCore, QtGui, QtWidgets
import progress_bar
import ui_effect


class ProgressDialog(QtWidgets.QDialog, progress_bar.Ui_Dialog):
    def __init__(self):
        super(ProgressDialog, self).__init__()
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)  # 透明
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 无边框
        self.label_background.setGraphicsEffect(ui_effect.shadow(0, 0, '#000000', 8))  # 阴影
        self.progressBar.setValue(0)

    def progress_update(self, value: int):
        self.progressBar.setValue(value)

