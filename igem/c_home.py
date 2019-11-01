import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtCore, QtGui, QtWidgets
import home
import ui_effect
from Backend import Backend


class HomePageWidget(QtWidgets.QWidget, home.Ui_HomeWidget):
    def __init__(self, backend: Backend):
        super(HomePageWidget, self).__init__()
        self.setupUi(self)
        self.backend = backend
        # 设置阴影
        self.button_encode.setGraphicsEffect(ui_effect.shadow(4, 4, '#101010', 8))
        self.button_decode.setGraphicsEffect(ui_effect.shadow(4, 4, '#101010', 8))
        # 设置图标
        self.button_encode.setIcon(QtGui.QIcon("resources/encode.png"))
        self.button_encode.setIconSize(QtCore.QSize(423, 542))
        self.button_decode.setIcon(QtGui.QIcon("resources/decode.png"))
        self.button_decode.setIconSize(QtCore.QSize(423, 542))
