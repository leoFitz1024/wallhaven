import _thread
import sys
from http.server import HTTPServer
from threading import Thread

from Ratio_Frame import Ui_Ratio_Frame
from PyQt5 import QtWidgets

from lib.HttpHandler import HttpHandler
from main_webview import Ui_MainWindow


def start_http(port):
    httpd = HTTPServer(('127.0.0.1', port), HttpHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    server = Thread(target=start_http, args=[1746])
    server.start()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.bind_event()
    MainWindow.show()
    status = 0
    sys.exit(app.exec_())
    #
    # app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # rf = Ratio_Frame()
    # rf.show()
    # MainWindow.show()
    # sys.exit(app.exec_())
