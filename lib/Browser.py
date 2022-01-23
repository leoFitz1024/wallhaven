import sys
from time import sleep

from PyQt5 import QtWebEngineWidgets, QtCore, QtWidgets
from PyQt5.QtCore import QUrl, QObject
from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem
from PyQt5.QtWidgets import QMenu, QMainWindow, QApplication


class Browser(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent=None):
        super(Browser, self).__init__(parent)

    def setCore(self, core):
        self.core = core

    def contextMenuEvent(self, event):
        self.menus = QMenu()
        self.menus.addAction('Save Image')
        self.menus.popup(event.globalPos())

    def download_file(self, url, filename, _self, function):
        print("download_file")
        q_url = QUrl("http://mirrors.aliyun.com/centos/7/isos/x86_64/CentOS-7-x86_64-Everything-2009.iso")
        try:
            print(self.page)
            self.page().download(q_url)
            print("start")
            self.downloadFunctionMap[url] = function
            self.selfMap[url] = _self
            self.page().profile().downloadRequested.connect(self.download_function)
        except OSError as e:
            print(e)

    def download_function(self, downloadItem: QWebEngineDownloadItem):
        print(download_function)
        function = self.downloadFunctionMap.pop(downloadItem.url().url())
        _self = self.selfMap.pop(downloadItem.url().url())
        function(_self, downloadItem)
        pass


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setObjectName("MainWindow")
        self.resize(1550, 840)
        self.setMinimumSize(QtCore.QSize(1200, 500))
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.browser = Browser(self.centralwidget)
        self.browser.setObjectName("browser")
        self.horizontalLayout.addWidget(self.browser)
        self.setCentralWidget(self.centralwidget)
        self.page = self.browser.page()
        self.setCentralWidget(self.browser)
        self.browser.load(QUrl("http://www.baidu.com.com"))
        self.show()
        self.start_d()

    def start_d(self):
        self.download()

    def download(self):
        print("2")
        q_url = QUrl("http://wppkg.baidupcs.com/issue/netdisk/yunguanjia/BaiduNetdisk_6.9.4.1.exe")
        self.page.download(q_url, filename='test_download')
        print("3")
        self.page.profile().downloadRequested.connect(self.downloadFucntion)

    def downloadFucntion(self, downloadItem: QWebEngineDownloadItem):
        print("xxx")
        print(downloadItem.path())
        print(downloadItem.url())
        print(downloadItem.totalBytes())
        print(downloadItem.totalBytes())
        print(downloadItem.downloadFileName())
        print(downloadItem.downloadDirectory())
        downloadItem.accept()


class Downloader(QObject):
    def __init__(self, page=None):
        super().__init__()
        self.page = page
        self.downloadFunctionMap = {}
        self.selfMap = {}

    def download(self, url, filename, _self, function):
        q_url = QUrl("http://mirrors.aliyun.com/centos/7/isos/x86_64/CentOS-7-x86_64-Everything-2009.iso")
        try:
            print(self.page)
            self.page.download(q_url, filename=filename)
            print("start")
            self.downloadFunctionMap[url] = function
            self.selfMap[url] = _self
            self.page.profile().downloadRequested.connect(self.download_function)
        except OSError as e:
            print(e)

    def download_function(self, downloadItem: QWebEngineDownloadItem):
        print(download_function)
        function = self.downloadFunctionMap.pop(downloadItem.url().url())
        _self = self.selfMap.pop(downloadItem.url().url())
        function(_self, downloadItem)
        pass
        # self.downloadItem.downloadProgress.connect(self.downloadProcess)
        # self.downloadItem.accept()

    def download_process(self, bytesReceived, bytesTotal):
        if self.on_process is not None:
            self.on_process(bytesReceived, bytesTotal)
        print(f"bytesReceived:{bytesReceived}==bytesTotal:{bytesTotal}")

    def pause(self):
        print("中断")
        sleep(10)
        self.downloadItem.pause()

    def resume(self):
        sleep(15)
        print("继续")
        print(self.downloadItem.isPaused())
        self.downloadItem.resume()


def download_function(downloadItem: QWebEngineDownloadItem):
    print("xx")
    downloadItem.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Context Menu test")
    # downloader = Downloader()
    # downloader.show()
    # _thread.start_new_thread(downloader.pause, ())
    # _thread.start_new_thread(downloader.resume, ())
    # downloader.download("http://mirrors.aliyun.com/centos/7/isos/x86_64/CentOS-7-x86_64-Everything-2009.iso",
    #                     "te", download_function)

    window = MainWindow()
    # window.start_d()
    sys.exit(app.exec_())
