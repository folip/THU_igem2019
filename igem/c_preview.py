import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtCore, QtGui, QtWidgets
import preview
from Backend import Backend
import ui_effect
from PIL import ImageQt


class PreviewWidget(QtWidgets.QWidget, preview.Ui_PreviewWidget):
    def __init__(self, backend: Backend):
        super(PreviewWidget, self).__init__()
        self.setupUi(self)
        self.backend = backend
        self.current_img = 0
        self.code_mode = ''
        self.timer = QtCore.QTimer()
        self.alarm_opacity = 150

        self.label_num2.setText('')
        self.label_num3.setText('')
        self.label_num4.setText('')
        self.label_num5.setText('')
        self.label_num6.setText('')
        self.label_num7.setText('')
        self.widget_prob.setVisible(False)
        self.label_file_alarm.setVisible(False)
        self.pushButton_next.setIcon(QtGui.QIcon('resources/right.png'))
        self.pushButton_next.setIconSize(QtCore.QSize(70, 70))

        self.pushButton_export.clicked.connect(self.export)
        self.pushButton_synthesis.clicked.connect(self.synthesis)
        self.pushButton_next.clicked.connect(self.next)
        self.timer.timeout.connect(self.alarm_disappear)

    def start_encoding(self, mode, result):
        self.code_mode = mode
        coding_result = result
        lengths = coding_result['segments']
        for i in range(5):
            lengths[i+1] += lengths[i]
        for i in range(6):
            lengths[i] = int(lengths[i] * 761 / lengths[5])
        structure_img = ui_effect.dna_structure(lengths)
        structure_qimg = ImageQt.ImageQt(structure_img)
        img = QtGui.QImage(structure_qimg)
        pixmap = QtGui.QPixmap.fromImage(img)
        self.label_dna_structure.setPixmap(pixmap)
        self.label_num2.move(lengths[0] - 4, 30)
        self.label_num2.setText(str(lengths[0]))
        self.label_num3.move(lengths[1] - 4, 30)
        self.label_num3.setText(str(lengths[1]))
        self.label_num4.move(lengths[2] - 4, 30)
        self.label_num4.setText(str(lengths[2]))
        self.label_num5.move(lengths[3] - 4, 30)
        self.label_num5.setText(str(lengths[3]))
        self.label_num6.move(lengths[4] - 4, 30)
        self.label_num6.setText(str(lengths[4]))
        self.label_num7.move(lengths[5] - 4, 30)
        self.label_num7.setText(str(lengths[5]))
        self.label_chunk_num.setText(str(coding_result['chunk_num']))
        self.label_oligo_num.setText(str(coding_result['oligo_num']))
        img = QtGui.QImage()
        img.load("figure/ori_dna.jpg")
        img = img.scaled(761, 421,
                         QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        self.label_2.setPixmap(QtGui.QPixmap.fromImage(img))
        self.current_img = 0
        self.label_3.setText(coding_result['info'])

    def export(self):
        save_path, save_type = QtWidgets.QFileDialog.getSaveFileName(self, 'export to...', '.')
        print(save_path)
        self.backend.save_encoding_result(save_path)
        self.export_finish_alarm()

    def synthesis(self):
        self.backend.save_encoding_result()

    def next(self):
        print(self.current_img)
        if self.current_img == 0:
            print(1)
            name_dic = {'DNA Fountain': 'FT_encoded_dna.jpg', 'DNA FT': 'masked_dna.jpg'}
            path = 'figure/' + name_dic[self.code_mode]
            img = QtGui.QImage()
            img.load(path)
            img = img.scaled(761, 421,
                             QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            self.label_2.setPixmap(QtGui.QPixmap.fromImage(img))
            self.current_img = 1
        else:
            print(2)
            img = QtGui.QImage()
            img.load("figure/ori_dna.jpg")
            img = img.scaled(761, 421,
                             QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            self.label_2.setPixmap(QtGui.QPixmap.fromImage(img))
            self.current_img = 0

    def export_finish_alarm(self):
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