import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtCore, QtGui, QtWidgets
import encode
import ui_effect
from c_config import ConfigDialog
from Backend import Backend
from FT_class import process as process_ft
from DNAMask import process as process_mk


# class RunCoding(QtCore.QThread):
#     def __init__(self, backend: Backend):
#         super(RunCoding, self).__init__()
#         self.backend = backend
#         self.trigger = QtCore.pyqtSignal()
#
#     def run(self):
#         result = self.backend.start_encoding()
#         pass
#         self.trigger.emit()
#         return result

class EncodeWidget(QtWidgets.QWidget, encode.Ui_EncodeWidget):
    drag_enter = False
    text = ''
    path = ''
    config_dic = {}
    config_dialog = None
    new_dialog = None
    config_text_ft = """# fountain code parameters
# encoding parameters
chunk_size: 24 @INT
rs_length: 2 @INT
alpha: 0.2 @FLOAT
# encryption parameters
mask: 81721121 @INT
a: 182121 @INT
n: 213123212 @INT
# scanning parameters
gc: 0.45,0.55 @INTERVAL
max_homo_length: 3 @INT
# primer
forward_primer: ATTGCTACACACACG @STR
reverse_primer: TCAGTCACTACGTAC @STR"""
    config_text_mk = """# fountain code parameters
# encoding parameters
chunk_size: 24 @INT
rs_length: 2 @INT
alpha: 0.2 @FLOAT
# encryption parameters
mask: 81721121 @INT
a: 182121 @INT
n: 213123212 @INT
# scanning parameters
gc: 0.45,0.55 @INTERVAL
max_homo_length: 3 @INT
# primer
forward_primer: ATTGCTACACACACG @STR
reverse_primer: TCAGTCACTACGTAC @STR"""

    def __init__(self, backend: Backend):
        super(EncodeWidget, self).__init__()
        self.alarm_opacity = 100
        self.setupUi(self)
        self.backend = backend
        # self.run_coding = RunCoding(self.backend)
        print(self.backend.dic)
        self.setAcceptDrops(True)
        self.mode = 'DNA Fountain'
        self.config_str2dic(self.config_text_ft)
        self.label_file_alarm.setVisible(False)
        self.timer = QtCore.QTimer()
        self.timer_process = QtCore.QTimer()
        # 阴影与图标
        self.widget_size.setGraphicsEffect(ui_effect.shadow(4, 4, '#101010', 8))
        self.pushButton_icon_file.setIcon(QtGui.QIcon('resources/file.png'))
        self.pushButton_icon_file.setIconSize(QtCore.QSize(56, 56))
        self.pushButton_icon_array.setIcon(QtGui.QIcon('resources/right_array.png'))
        self.pushButton_icon_array.setIconSize(QtCore.QSize(56, 56))
        self.pushButton_icon_dna.setIcon(QtGui.QIcon('resources/dna.png'))
        self.pushButton_icon_dna.setIconSize(QtCore.QSize(56, 56))
        self.widget_chunks.setGraphicsEffect(ui_effect.shadow(4, 4, '#101010', 8))
        self.widget_config.setGraphicsEffect(ui_effect.shadow(4, 4, '#101010', 8))
        self.pushButton_start.setGraphicsEffect(ui_effect.shadow(4, 4, '#101010', 8))
        self.pushButton_icon_fountain.setIcon(QtGui.QIcon('resources/water_white.png'))
        self.pushButton_icon_fountain.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_icon_mask.setIcon(QtGui.QIcon('resources/mask_white.png'))
        self.pushButton_icon_mask.setIconSize(QtCore.QSize(50, 50))
        self.label_loading_background.setGraphicsEffect(ui_effect.shadow(4, 4, '#101010', 8))
        self.pushButton_loading_icon.setIcon(QtGui.QIcon('resources/loading.gif'))
        self.pushButton_loading_icon.setIconSize(QtCore.QSize(56, 56))
        self.label_loading_background.setVisible(False)
        self.label_loading_text.setVisible(False)
        self.pushButton_loading_icon.setVisible(False)
        # 槽
        self.pushButton_icon_fountain.clicked.connect(self.set_config)
        self.pushButton_icon_mask.clicked.connect(self.set_config)
        self.timer.timeout.connect(self.alarm_disappear)
        # self.timer_process.timeout.connect(self.process_update)


    def dragEnterEvent(self, QDragEnterEvent):
        self.drag_enter = True
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
        change_result = self.backend.change_file_name(self.path)
        if change_result:
            self.label_CG_chunks.setText(str(change_result['gc_out_of_range']))
            self.label_homo_chunks.setText(str(change_result['chunks_with_long_homo']))
            self.label_file_size.setText(str(change_result['file_size']))
            self.label_chunk_num.setText(str(change_result['chunk_num']))
            img_cg = QtGui.QImage()
            img_cg.load("figure/gc.jpg")
            img_cg = img_cg.scaled(258, 194, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            img_homo = QtGui.QImage()
            img_homo.load("figure/homo.jpg")
            img_homo = img_homo.scaled(258, 194, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            self.label_CG_graph.setPixmap(QtGui.QPixmap.fromImage(img_cg))
            self.label_homo_graph.setPixmap((QtGui.QPixmap.fromImage(img_homo)))
        QDropEvent.accept()

    def set_config(self):
        sender_dict = {'pushButton_icon_fountain': 0,
                       'pushButton_icon_mask': 1}
        index = sender_dict[self.sender().objectName()]
        if index:
            self.pushButton_icon_fountain.setIcon(QtGui.QIcon('resources/water_white.png'))
            self.pushButton_icon_fountain.setIconSize(QtCore.QSize(50, 50))
            self.pushButton_icon_mask.setIcon(QtGui.QIcon('resources/mask_red.png'))
            self.pushButton_icon_mask.setIconSize(QtCore.QSize(50, 50))
        else:
            self.pushButton_icon_fountain.setIcon(QtGui.QIcon('resources/water_blue.png'))
            self.pushButton_icon_fountain.setIconSize(QtCore.QSize(50, 50))
            self.pushButton_icon_mask.setIcon(QtGui.QIcon('resources/mask_white.png'))
            self.pushButton_icon_mask.setIconSize(QtCore.QSize(50, 50))
        if index:
            text_preview = self.config_text_ft
            text, result = ConfigDialog.text(text_preview)
            self.config_text_ft = text
        else:
            text_preview = self.config_text_mk
            text, result = ConfigDialog.text(text_preview)
            self.config_text_mk = text
        method = ['DNA Fountain', 'DNA Mask']
        self.mode = method[index]
        if result:
            self.config_received(text)
        else:
            self.pushButton_icon_fountain.setIcon(QtGui.QIcon('resources/water_white.png'))
            self.pushButton_icon_fountain.setIconSize(QtCore.QSize(50, 50))
            self.pushButton_icon_mask.setIcon(QtGui.QIcon('resources/mask_white.png'))
            self.pushButton_icon_mask.setIconSize(QtCore.QSize(50, 50))

    def config_received(self, text):
        self.config_str2dic(text)
        change_result = self.backend.change_config(self.config_dic)
        if change_result:
            self.label_CG_chunks.setText(str(change_result['gc_out_of_range']))
            self.label_homo_chunks.setText(str(change_result['chunks_with_long_homo']))
            self.label_file_size.setText(str(change_result['file_size']))
            self.label_chunk_num.setText(str(change_result['chunk_num']))

    def config_str2dic(self, config_text: str):
        lines = config_text.split('\n')
        for line in lines:
            line_cleared = line.replace(' ', '')
            if line_cleared[0] != '#':
                line_cleared, typ = line_cleared.split('@')
                key, value = line_cleared.split(':')
                if typ == 'INT':
                    value = int(value)
                elif typ == 'FLOAT':
                    value = float(value)
                elif typ == 'INTERVAL':
                    value = [float(i) for i in value.split(',')]
                self.config_dic[key] = value
        self.config_dic['encoding method'] = self.mode

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

    def start_encoding(self):
        self.label_loading_background.setVisible(True)
        self.label_loading_text.setVisible(True)
        self.pushButton_loading_icon.setVisible(True)
        # self.timer_process.start(50)

        result = self.backend.start_encoding()
        # self.label_loading_background.setVisible(False)
        # self.label_loading_text.setVisible(False)
        # self.pushButton_loading_icon.setVisible(False)

        # result = self.run_coding.start()
        # self.run_coding.trigger.connect(self.coding_finish)
        return result

    # def coding_finish(self):
    #     self.timer_process.stop()
    #
    # def process_update(self):
    #     if self.mode == 'DNA Fountain':
    #         print(str(process_ft) + 'front')
    #         if process_ft >= 100:
    #             self.timer_process.stop()
    #     else:
    #         print(process_mk)
    #         if process_mk >= 100:
    #             self.timer_process.stop()
