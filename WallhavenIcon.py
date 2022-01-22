import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication, qApp

from lib.Browser import MainWindow
from lib.WallhavenV2 import WallhavenV2
from main_browser import Ui_MainWindow


class WallhavenIcon(QSystemTrayIcon):
    def __init__(self, mainWindow: WallhavenV2, parent=None):
        super(WallhavenIcon, self).__init__(parent)
        self.my_icon = QIcon(f'{os.getcwd()}/icon/icon.png')
        self.createMenu()
        self.mainWindow = mainWindow

    def createMenu(self):
        self.menu = QMenu()
        self.index = QAction("首页", self, triggered=self.showMain)
        self.last = QAction("上一张", self, triggered=self.last_bg)
        self.next = QAction("下一张", self, triggered=self.next_bg)
        self.dislike = QAction("不喜欢这张", self, triggered=self.dislike_cur)
        # self.setting = QAction("设置", self, triggered=self.showSetting)
        self.quitAction = QAction("退出", self, triggered=self.quit)

        self.menu.addAction(self.index)
        self.menu.addAction(self.last)
        self.menu.addAction(self.next)
        self.menu.addAction(self.dislike)
        # self.menu.addAction(self.setting)
        self.menu.addAction(self.quitAction)
        self.setContextMenu(self.menu)

        # 设置图标
        self.setToolTip("打开主页面")
        self.setIcon(self.my_icon)
        self.icon = self.MessageIcon()

        # 把鼠标点击图标的信号和槽连接
        self.activated.connect(self.onIconClicked)

    # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
    def onIconClicked(self, reason):
        if reason == 2 or reason == 3:
            self.showMain()

    def showMain(self):
        self.mainWindow.show()

    def next_bg(self):
        self.mainWindow.next_bg()

    def last_bg(self):
        self.mainWindow.last_bg()

    def dislike_cur(self):
        self.mainWindow.dislike_current()

    def quit(self):
        qApp.quit()
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setQuitOnLastWindowClosed(False)
    MainWindow = WallhavenV2()
    MainWindow.setupUi()
    icon = WallhavenIcon(MainWindow)
    MainWindow.setIcon(icon.my_icon)
    icon.show()
    MainWindow.show()
    sys.exit(app.exec_())
