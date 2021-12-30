import sys

from PyQt5 import QtWidgets

from lib.Ui_MainWindow import Ui_MainWindow
from lib.Wallhaven import Wallhaven

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    mainExe = Wallhaven()
    mainExe.load_config()
    ui = Ui_MainWindow(mainExe)
    ui.setupUi(MainWindow)
    ui.show()
    ui.init_ui_by_config()
    sys.exit(app.exec_())
