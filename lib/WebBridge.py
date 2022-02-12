# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal


class WebBridge(QObject):
    # to web
    SigAddDownloadTask = pyqtSignal(str)
    SigDownloadFinished = pyqtSignal(str)
    SigDownloadCanceled = pyqtSignal(str)
    SigImgFolderChanged = pyqtSignal(str)
    SigUpdatePageInfo = pyqtSignal(str)
    # web to qt
    SigSelectFolder = pyqtSignal(str)
    SigOpenFolder = pyqtSignal(str)
    # 窗口最小化信号
    windowMinimized = pyqtSignal()
    # 窗口最大化信号
    windowMaximized = pyqtSignal()
    # 窗口关闭信号
    windowClosed = pyqtSignal()

    def __init__(self):
        super(WebBridge, self).__init__()

    @pyqtSlot(str)
    def selectFolder(self, path):
        self.SigSelectFolder.emit(path)

    @pyqtSlot(str)
    def openFolder(self, path):
        self.SigOpenFolder.emit(path)

    @pyqtSlot(str)
    def minimizeWin(self):
        self.windowMinimized.emit()

    @pyqtSlot(str)
    def maximizeWin(self):
        self.windowMaximized.emit()

    @pyqtSlot(str)
    def closeWin(self):
        self.windowClosed.emit()



    #
    # @pyqtSlot(str)
    # def loadMoreData(self, page):
    #     print(page)
    #     self.SigLoadMoreData.emit(int(page))
    #
    # @pyqtSlot(str)
    # def downloadImg(self, url):
    #     print(url)
