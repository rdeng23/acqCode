import configparser
import socket
import threading

from PyQt6.QtCore import QObject, pyqtSignal

port = 6666

config = configparser.ConfigParser(allow_no_value=True)
config.read('/usr/local/large_dram_data_capture_fat/config.ini')
if 'server.udp' in config and 'port' in config['server.udp']:
    port = int(config['server.udp']['port'])


class Communicate(QObject):
    received = pyqtSignal(str)


class UdpSocket:

    def __init__(self):
        self.socket = None
        self.t = None
        self.c = Communicate()

    def init(self):
        # self.socket = QUdpSocket()
        # self.socket.bind(QHostAddress.SpecialAddress.Broadcast, port)
        # self.socket.readyRead.connect(self.on_udp_ready_read)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind(('0.0.0.0', port))
        self.on_udp_ready_read()

    def on_udp_ready_read(self):
        self.t = threading.Thread(target=self.on_udp_ready_read_run)
        self.t.daemon = True
        self.t.start()

    def on_udp_ready_read_run(self):
        while True:
            data, addr = self.socket.recvfrom(1024)
            self.c.received.emit(str(data, 'utf-8'))
        # while True:
        #     if self.socket.hasPendingDatagrams():
        #         datagram, host, port = self.socket.readDatagram(
        #             self.socket.pendingDatagramSize()
        #         )
        #         self.c.received.emit(str(datagram, 'utf-8'))
