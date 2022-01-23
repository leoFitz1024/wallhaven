# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QThread


class WebBridge(QObject):
    SigAddDownloadTask = pyqtSignal(str)
    SigDownloadFinished = pyqtSignal(str)
    SigDownloadCanceled = pyqtSignal(str)
    SigSelectFolder = pyqtSignal(str)
    SigImgFolderChanged = pyqtSignal(str)

    def __init__(self):
        super(WebBridge, self).__init__()

    @pyqtSlot(str)
    def selectFolder(self, path):
        print("selectFolder")
        self.SigSelectFolder.emit(path)
    #
    # @pyqtSlot(str)
    # def loadMoreData(self, page):
    #     print(page)
    #     self.SigLoadMoreData.emit(int(page))
    #
    # @pyqtSlot(str)
    # def downloadImg(self, url):
    #     print(url)
