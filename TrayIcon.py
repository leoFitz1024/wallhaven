import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication, qApp

from lib.Ui_MainWindow import Ui_MainWindow
from lib.Wallhaven import Wallhaven


class TrayIcon(QSystemTrayIcon):
    def __init__(self, mainWindow: Ui_MainWindow, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.my_icon = QIcon(f'{os.getcwd()}/icon/icon.png')
        self.createMenu()
        self.mainWindow = mainWindow

    def createMenu(self):
        self.menu = QMenu()
        self.last = QAction("上一张", self, triggered=self.last_bg)
        self.next = QAction("下一张", self, triggered=self.next_bg)
        self.dislike = QAction("不喜欢这张", self, triggered=self.dislike_cur)
        self.setting = QAction("设置", self, triggered=self.showSetting)
        self.quitAction = QAction("退出", self, triggered=self.quit)

        self.menu.addAction(self.last)
        self.menu.addAction(self.next)
        self.menu.addAction(self.dislike)
        self.menu.addAction(self.setting)
        self.menu.addAction(self.quitAction)
        self.setContextMenu(self.menu)

        # 设置图标
        self.setToolTip("点击切换壁纸")
        self.setIcon(self.my_icon)
        self.icon = self.MessageIcon()

        # 把鼠标点击图标的信号和槽连接
        self.activated.connect(self.onIconClicked)

    # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
    def onIconClicked(self, reason):
        if reason == 2 or reason == 3:
            self.next_bg()

    def showSetting(self):
        self.mainWindow.show_ui()

    def next_bg(self):
        self.mainWindow.mainExe.next_bg()

    def last_bg(self):
        self.mainWindow.mainExe.last_bg()

    def dislike_cur(self):
        self.mainWindow.mainExe.dislike_current()

    def quit(self):
        qApp.quit()
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setQuitOnLastWindowClosed(False)
    mainExe = Wallhaven()
    ui = Ui_MainWindow(mainExe)
    ui.init_Ui()
    ti = TrayIcon(ui)
    ui.setIcon(ti.my_icon)
    ti.show()
    ui.show_ui()
    sys.exit(app.exec_())
