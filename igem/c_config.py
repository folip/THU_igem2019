import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtCore, QtGui, QtWidgets
import config
import ui_effect
from Backend import Backend


class ConfigDialog(QtWidgets.QDialog, config.Ui_CodingConfigDialog):
    def __init__(self, backend: Backend, parent=None):
        super(ConfigDialog, self).__init__(parent)
        self.setupUi(self)
        self.backend = backend
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.label_background.setGraphicsEffect(ui_effect.shadow(0, 0, '#000000', 8))
        self.pushButton_ok.setGraphicsEffect(ui_effect.shadow(4, 4, '#101010', 8))
        self.pushButton_cancel.setGraphicsEffect(ui_effect.shadow(4, 4, '#101010', 8))
        self.pushButton_ok.clicked.connect(self.accept)
        self.pushButton_cancel.clicked.connect(self.reject)

    def get_text(self):
        return self.textEdit.toPlainText()

    def set_text(self, text):
        self.textEdit.setPlainText(text)

    @staticmethod
    def text(text_preview, parent=None):
        dialog = ConfigDialog(parent)
        dialog.set_text(text_preview)
        result = dialog.exec_()
        text = dialog.get_text()
        return text, result == QtWidgets.QDialog.Accepted
