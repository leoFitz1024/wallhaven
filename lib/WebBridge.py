# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QThread


class WebBridge(QObject):
    SigAddDownloadTask = pyqtSignal(str)
    SigDownloadFinished = pyqtSignal(str)
    SigDownloadCanceled = pyqtSignal(str)

    def __init__(self):
        super(WebBridge, self).__init__()

    # @pyqtSlot(str)
    # def saveBarParams(self, strParameter):
    #     self.SigSaveParamsFromWeb.emit(strParameter)
    #
    # @pyqtSlot(str)
    # def loadMoreData(self, page):
    #     print(page)
    #     self.SigLoadMoreData.emit(int(page))
    #
    # @pyqtSlot(str)
    # def downloadImg(self, url):
    #     print(url)
