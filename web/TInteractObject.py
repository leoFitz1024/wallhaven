from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class TInteractObj(QObject):
    # SigReceivedMessFromJS = pyqtSignal(str)
    SigSendMessageToJS = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(str)
    def JSSendMessage(self, strParameter):
        print('JSSendMessage(%s) from Html' % strParameter)
        # self.SigReceivedMessFromJS.emit(strParameter)

    @pyqtSlot(result=str)
    def fun(self):
        print('TInteractObj.fun()')
        return 'hello'