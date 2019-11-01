import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtCore, QtGui, QtWidgets
import decode
import ui_effect
from c_config import ConfigDialog
from Backend import Backend


class DecodeWidget(QtWidgets.QWidget, decode.Ui_DecodeWidget):
    def __init__(self, backend: Backend):
        super(DecodeWidget, self).__init__()
        self.backend = backend
        self.setupUi(self)
        self.alarm_opacity = 100
        self.setAcceptDrops(True)
        self.label_file_alarm.setVisible(False)
        self.timer = QtCore.QTimer()
        self.text = ''
        self.path = ''

        self.label_loading_background.setGraphicsEffect(ui_effect.shadow(4, 4, '#101010', 8))
        self.pushButton_loading_icon.setIcon(QtGui.QIcon('resources/loading.gif'))
        self.pushButton_loading_icon.setIconSize(QtCore.QSize(56, 56))
        self.label_loading_background.setVisible(False)
        self.label_loading_text.setVisible(False)
        self.pushButton_loading_icon.setVisible(False)

        self.timer.timeout.connect(self.alarm_disappear)
        self.pushButton_start.clicked.connect(self.start)

    def dragEnterEvent(self, QDragEnterEvent):
        self.text = QDragEnterEvent.mimeData().text()
        QDragEnterEvent.accept()

    def dropEvent(self, QDropEvent):
        self.path = self.text.replace('file:///', '')
        name = self.path.split('/')[-1]
        self.label_file_name.setText(name)
        if self.path.split('.')[-1] in ['jpg', 'png', 'jpeg', 'bmp']:
            img = QtGui.QImage()
            img.load(self.path)
            size = img.size()
            h_rate = size.height() / 341
            w_rate = size.width() / 526
            if (h_rate > w_rate) & (h_rate > 1):
                img = img.scaled(int(size.width() / h_rate), 341,
                                 QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            elif (h_rate <= w_rate) & (w_rate > 1):
                img = img.scaled(526, int(size.height() / w_rate),
                                 QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            self.label_preview.setPixmap(QtGui.QPixmap.fromImage(img))
        else:
            img = QtGui.QImage()
            img.load("resources/file.png")
            img = img.scaled(120, 120,
                             QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            self.label_preview.setPixmap(QtGui.QPixmap.fromImage(img))
        QDropEvent.accept()

    def start(self):
        if len(self.path) == 0:
            self.file_void_alarm()
        else:
            self.label_loading_background.setVisible(True)
            self.label_loading_text.setVisible(True)
            self.pushButton_loading_icon.setVisible(True)
            self.backend.decode(self.path)
            self.label_loading_background.setVisible(False)
            self.label_loading_text.setVisible(False)
            self.pushButton_loading_icon.setVisible(False)

    def file_void_alarm(self):
        self.label_file_alarm.setVisible(True)
        self.alarm_opacity = 150
        self.timer.start(20)

    def alarm_disappear(self):
        self.alarm_opacity -= 4
        if self.alarm_opacity <= 0:
            self.timer.stop()
            self.label_file_alarm.setVisible(False)
        else:
            op = QtWidgets.QGraphicsOpacityEffect()
            op.setOpacity(self.alarm_opacity / 100)
            self.label_file_alarm.setGraphicsEffect(op)
