from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget, QFormLayout, QRadioButton, QButtonGroup, QLabel, QPushButton

from ui import global_data


class Communicate(QObject):
    confirmed = pyqtSignal()


class AcqSelect(QWidget):
    def __init__(self, data):
        super().__init__()

        self.button = None
        self.c = Communicate()
        self.groupButton = QButtonGroup()
        self.emptyLabel = None
        self.layout = None
        self.box = None
        self.setWindowTitle('新窗口')
        self.resize(400, 400)
        self.data = data

        self.init_ui()

    def init_ui(self):
        self.box = QWidget(self)
        self.box.setGeometry(10, 10, 380, 400)

        self.layout = QFormLayout(self.box)

        if self.data is not None and len(self.data) > 0:
            for item in self.data:
                checkbox = QRadioButton(item)
                self.groupButton.addButton(checkbox)
                self.layout.addRow(checkbox)
            self.button = QPushButton("确认")
            self.layout.addRow(self.button)
            self.button.clicked.connect(self.confirm)

        else:
            emptyLabel = QLabel("未扫描到可用的设备")
            self.layout.addRow(emptyLabel)

    def confirm(self):
        if self.groupButton.checkedButton() is not None:
            global_data.set_acd_id(self.groupButton.checkedButton().text().split(" ")[2])
            self.c.confirmed.emit()
            self.close()
