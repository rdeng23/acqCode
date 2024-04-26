import sys

from PyQt6.QtWidgets import QApplication

from ui.MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
