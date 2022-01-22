import sys
from threading import Thread
from PyQt5 import QtWidgets

from lib.HttpServer import HttpServer
from main_browser import Ui_MainWindow


def start_http(port):
    HttpServer('11').start(port=port)


if __name__ == '__main__':
    server = Thread(target=start_http, args=[1746])
    server.setDaemon(True)
    server.start()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MainWindow()
    MainWindow.show()
    status = 0
    sys.exit(app.exec_())
