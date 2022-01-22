import sys

from PyQt5.QtWidgets import QApplication

from web.TMainWindow import TMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setQuitOnLastWindowClosed(False)
    MainWindow = TMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
