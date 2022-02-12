import logging
import os
import time
import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtNetwork import QLocalServer, QLocalSocket
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication, qApp
import cherrypy
import cherrypy.wsgiserver.wsgiserver3

from lib.WallhavenV2 import WallhavenV2


class WallhavenIcon(QSystemTrayIcon):
    def __init__(self, mainWindow: WallhavenV2, parent=None):
        super(WallhavenIcon, self).__init__(parent)
        self.mainWindow = mainWindow

    def init_data(self, path):
        self.ABSPATH = path
        self.my_icon = QIcon(f'{path}/icon/icon.png')
        self.createMenu()

    def createMenu(self):
        self.menu = QMenu()
        self.index = QAction("首页", self, triggered=self.showMain)
        self.last = QAction("上一张", self, triggered=self.last_bg)
        self.next = QAction("下一张", self, triggered=self.next_bg)
        # self.dislike = QAction("不喜欢这张", self, triggered=self.dislike_cur)
        # self.setting = QAction("设置", self, triggered=self.showSetting)
        self.quitAction = QAction("退出", self, triggered=self.quit)

        self.menu.addAction(self.index)
        self.menu.addAction(self.last)
        self.menu.addAction(self.next)
        # self.menu.addAction(self.dislike)
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
        self.mainWindow.showNormal()

    def show_min_message(self):
        self.showMessage("提示", "Wallhaven已最小化到托盘", self.icon)

    def next_bg(self):
        self.mainWindow.next_bg()

    def last_bg(self):
        self.mainWindow.last_bg()

    def dislike_cur(self):
        self.mainWindow.dislike_current()

    def quit(self):
        qApp.quit()
        sys.exit()


def init_logger(abs_path):
    # 第一步，创建一个logger
    logger = logging.getLogger("WallHaven")
    logger.setLevel(logging.INFO)  # Log等级总开关
    # 第二步，创建一个handler，用于写入日志文件
    rq = time.strftime('%Y%m', time.localtime(time.time()))
    log_path = os.path.join(abs_path, 'logs')
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_name = os.path.join(log_path, rq + '.log')
    logfile = log_name
    # 到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  # 输出到console的log等级的开关
    # 到文件
    fh = logging.FileHandler(logfile, mode='a+')
    fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
    # 第三步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # 第四步，将logger添加到handler里面
    logger.addHandler(fh)
    logger.addHandler(ch)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    serverName = 'wallhaven-sever-f4sdf5sa42s4fa52s4fw'
    socket = QLocalSocket()
    socket.connectToServer(serverName)
    # 如果连接成功，表明server已经存在，当前已有实例在运行
    if socket.waitForConnected(500):
        QtWidgets.QMessageBox.critical(None, "提示", "Wallhaven已经运行。")
        app.quit()
        sys.exit()
    # 没有实例运行，创建服务器
    localServer = QLocalServer()
    localServer.listen(serverName)
    state = 0
    try:
        QApplication.setQuitOnLastWindowClosed(False)
        app.senderSignalIndex()
        exe_path = sys.argv[0]
        abs_path = os.path.abspath(os.path.dirname(exe_path) + os.path.sep + ".")
        init_logger(abs_path)
        MainWindow = WallhavenV2()
        MainWindow.setupUi()
        MainWindow.init_path(exe_path, abs_path)
        trayIcon = WallhavenIcon(MainWindow)
        trayIcon.init_data(abs_path)
        MainWindow.setIcon(trayIcon.my_icon)
        trayIcon.show()
        if not (len(sys.argv) > 1 and sys.argv[1] == 'AutoRun'):
            MainWindow.show()
        else:
            trayIcon.show_min_message()
        state = app.exec_()
    except Exception as e:
        print(e)
    finally:
        localServer.close()
        sys.exit(state)



