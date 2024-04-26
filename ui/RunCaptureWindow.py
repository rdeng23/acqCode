from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QPushButton, QLabel, QWidget, QLineEdit, \
    QFormLayout, QSpinBox

from ui import global_data


class Communicate(QObject):
    confirmed = pyqtSignal()


class RunCaptureWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.p = None
        self.c = Communicate()
        self.socket = None
        self.layout = None
        self.box = None
        self.setWindowTitle('新窗口')
        self.resize(400, 400)

        self.btnConfirm = QPushButton('确定', self)

        args = global_data.get_args()

        spad = args['spad'] if 'spad' in args else ''
        self.labelSpad = QLabel('spad')
        self.inputSpad = QLineEdit(spad, self)

        commsA = args['commsA'] if 'commsA' in args else ''
        self.labelCommsA = QLabel('commsA')
        self.inputCommsA = QLineEdit(commsA, self)

        decimate = args['decimate'] if 'decimate' in args else ''
        self.labelDecimate = QLabel('decimate')
        self.inputDecimate = QLineEdit(decimate, self)

        trg = args['trg'] if 'trg' in args else ''
        self.labelTrg = QLabel('trg')
        self.inputTrg = QLineEdit(trg, self)

        secs = args['secs'] if 'secs' in args else 1
        self.labelSecs = QLabel('secs')
        self.inputSecs = QSpinBox(self)
        self.inputSecs.setValue(int(secs))
        self.inputSecs.setMinimum(1)
        self.inputSecs.setMaximum(5)
        self.inputSecs.setFixedWidth(50)

        self.labelOther = QLabel('other')
        self.inputOther = QLineEdit(global_data.get_args_other(), self)

        self.labelResult = QLabel()
        self.runStatus = QLabel()

        self.init_ui()

    def init_ui(self):
        self.box = QWidget(self)
        self.box.setGeometry(10, 10, 380, 400)

        self.btnConfirm.clicked.connect(self.confirm)

        self.layout = QFormLayout(self.box)
        self.inputSpad.setFixedWidth(280)
        self.inputCommsA.setFixedWidth(280)
        self.inputDecimate.setFixedWidth(280)
        self.inputTrg.setFixedWidth(280)
        self.inputOther.setFixedWidth(280)

        self.layout.addRow(self.labelSpad, self.inputSpad)
        self.layout.addRow(self.labelCommsA, self.inputCommsA)
        self.layout.addRow(self.labelDecimate, self.inputDecimate)
        self.layout.addRow(self.labelTrg, self.inputTrg)
        self.layout.addRow(self.labelSecs, self.inputSecs)
        self.layout.addRow(self.labelOther, self.inputOther)
        self.layout.addRow(self.btnConfirm)
        self.layout.addRow(self.labelResult)
        self.layout.addRow(self.runStatus)

    def confirm(self):
        args = {
            'spad': self.inputSpad.text(),
            'commsA': self.inputCommsA.text(),
            'decimate': self.inputDecimate.text(),
            'trg': self.inputTrg.text(),
            'secs': self.inputSecs.text()
        }
        global_data.set_args(args)
        global_data.set_args_other(self.inputOther.text())
        self.c.confirmed.emit()
