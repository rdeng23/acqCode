import configparser
import pathlib
import threading

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QPushButton, QMainWindow, QMessageBox, QLabel, QFileDialog

import device_api
from net.UdpSocket import UdpSocket
from output import reAssembleFile
from ui import global_data
from ui.AcqSelect import AcqSelect
from ui.RunCaptureWindow import RunCaptureWindow

config_path = "/usr/local/large_dram_data_capture_fat/config.ini"

CHANNEL_COUNT_2106 = 192

origin_date_file = "/mnt/{}/afhba.0/{}/000001/0.00"
out_path = "/dram_data"

das_address = "//192.168.1.4/2mdas"
das_username = "Administrator"
das_password = "dalleote"
das_mount_path = "/das/data"


def get_config(module, key, default_value):
    if module in config:
        if key in config[module]:
            return config[module][key]
    return default_value


file_obj = pathlib.Path(config_path)
if file_obj.exists():
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(config_path)

    origin_date_file = get_config('data', 'origin_date_file', origin_date_file)
    out_path = get_config('data', 'out_path', out_path)

    das_address = get_config('das', 'das_address', das_address)
    das_username = get_config('das', 'das_username', das_username)
    das_password = get_config('das', 'das_password', das_password)
    das_mount_path = get_config('das', 'das_mount_path', das_mount_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.socket = None
        self.p = None
        self.labelPing = None
        self.labelLoadNirq = None
        self.labelFirmware = None
        self.wConfigForm = None
        self.labelConfigForm = None
        self.btnRun = None
        self.labelRun = None
        self.wAcpSelect = None
        self.runStatus = QLabel()

        self.socket = UdpSocket()
        self.socket.init()
        self.socket.c.received.connect(self.on_message)

        self.init_ui()

    def init_ui(self):
        act_version = QAction('&Version', self)
        act_version.triggered.connect(self.show_version)
        menubar = self.menuBar()
        aboutMenu = menubar.addMenu("About")
        aboutMenu.addAction(act_version)

        btn_show_firmware = QPushButton('获取AFHBA404固件版本', self)
        btn_show_firmware.move(10, 30)
        btn_show_firmware.setFixedSize(200, 30)
        btn_show_firmware.clicked.connect(self.show_firmware)

        self.labelFirmware = QLabel("<firmware>", self)
        self.labelFirmware.move(250, 30)
        self.labelFirmware.setFixedSize(400, 30)

        btn_loadNIRQ = QPushButton('加载数采设备', self)
        btn_loadNIRQ.move(10, 80)
        btn_loadNIRQ.setFixedSize(200, 30)
        btn_loadNIRQ.clicked.connect(self.load_nirq)
        self.labelLoadNirq = QLabel("<加载数采设备>", self)
        self.labelLoadNirq.move(250, 80)
        self.labelLoadNirq.setFixedSize(400, 30)

        btn_pingACQ = QPushButton('检查网口连接', self)
        btn_pingACQ.move(10, 130)
        btn_pingACQ.setFixedSize(200, 30)
        btn_pingACQ.clicked.connect(self.ping_acq)
        self.labelPing = QLabel("<ping here>", self)
        self.labelPing.move(250, 130)
        self.labelPing.setFixedSize(400, 30)

        btn_run_capture = QPushButton('任务配置', self)
        btn_run_capture.move(10, 180)
        btn_run_capture.setFixedSize(200, 30)
        btn_run_capture.clicked.connect(self.run_capture)
        self.labelConfigForm = QLabel(self)
        self.labelConfigForm.move(250, 180)
        self.labelConfigForm.setFixedSize(500, 30)

        self.btnRun = QPushButton('启动任务', self)
        self.btnRun.move(10, 230)
        self.btnRun.setFixedSize(200, 30)
        self.labelRun = QLabel(self)
        self.labelRun.move(250, 230)
        self.labelRun.setFixedSize(300, 30)
        self.btnRun.clicked.connect(self.run)

        self.runStatus.move(10, 330)
        self.runStatus.setFixedSize(500, 30)

        self.statusBar()
        self.setFixedWidth(800)
        self.setFixedHeight(500)
        self.setWindowTitle("D-TACQ Streaming")
        self.show()

    def show_version(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Info")
        dlg.setText("Version: 1.0.1 \nAuther: rdeng")
        dlg.exec()

    def show_firmware(self):
        self.labelFirmware.setText(device_api.afhba404_get_ident())

    def load_nirq(self):
        load_res = device_api.load_nirq()
        if load_res.fail():
            self.labelLoadNirq.setText(load_res.message)
            return
        mnt_res = device_api.mount_ramdisk()
        if mnt_res.fail():
            self.labelLoadNirq.setText(mnt_res.message)
            return
        res = device_api.get_ident_all()
        if res.success():
            self.wAcpSelect = AcqSelect(res.model)
            self.wAcpSelect.show()
            self.wAcpSelect.c.confirmed.connect(self.checked_acq)

    def ping_acq(self):
        acq_result = device_api.ping_acq(global_data.get_acd_id())
        das_result = device_api.mount_das(das_address, das_username, das_password, das_mount_path)
        self.labelPing.setText("T-DACQ: {}, DAS: {}".format(acq_result, das_result))

    def run_capture(self):
        self.wConfigForm = RunCaptureWindow()
        self.wConfigForm.show()
        self.wConfigForm.c.confirmed.connect(self.show_args)

    def select_driver(self):
        p = QFileDialog().getExistingDirectory(self, "选择文件", "~")
        device_api.change_driver_path(p)
        self.textDriver.setText(device_api.get_driver_path())

    def show_args(self):
        self.wConfigForm.hide()
        args = global_data.get_args()
        keys = args.keys()
        text = ''
        if len(keys) > 0:
            for key in keys:
                if key != '':
                    text += key + ':' + args[key] + ', '
        if global_data.get_args_other() != '':
            text += 'other:' + global_data.get_args_other()
        self.labelConfigForm.setText(text)

    def run(self):
        if self.btnRun.text() == '启动任务':
            global_data.set_running(True)
            self.btnRun.setText('停止任务')
            self.labelRun.setWordWrap(True)
            self.labelRun.setText("任务就绪，等待开启指令")
        else:
            global_data.set_running(False)
            self.btnRun.setText('启动任务')
            self.labelRun.setText('')

    def on_message(self, command):
        if global_data.get_running() & (global_data.get_receiving() is False):
            global_data.set_receiving(True)
            self.labelRun.setText("已接收到指令：" + command)
            arr = command.split(',')
            if arr[0] == 'Datarefresh':
                args = global_data.get_args()
                args['p'] = arr[1]
                args['secs'] = arr[2]
                self.p = device_api.acq2106_hts(global_data.get_args(), global_data.get_acd_id(),
                                                global_data.get_args_other())
                threading.Thread(target=self.read).start()
                threading.Thread(target=self.err).start()

    def read(self):
        if self.p is not None and self.p.stdout is not None and self.p.stdout.closed is not True:
            while True:
                line = self.p.stdout.readline()
                print(line)
                if not line:
                    break
                self.runStatus.setText(str(line))
                if 'stop_shot' in str(line, 'utf-8'):
                    args = global_data.get_args()

                    self.labelRun.setText("接收完成，开始转存数据，请稍等...")
                    reAssembleFile(
                        origin_date_file.format(args["p"], global_data.get_acd_id()),
                        CHANNEL_COUNT_2106,
                        int(args["secs"]),
                        int(args["p"]),
                        out_path,
                        das_addbase
                    )

                    global_data.set_receiving(False)
                    self.labelRun.setText("任务已完成，任务再次就绪，等待开启指令")

    def err(self):
        if self.p is not None and self.p.stderr is not None and self.p.stderr.closed is not True:
            line = ''
            while True:
                r = self.p.stderr.readline()
                if not r:
                    break
                line += str(r)
                self.runStatus.setText(line)

    def checked_acq(self):
        self.labelLoadNirq.setText(global_data.get_acd_id())
