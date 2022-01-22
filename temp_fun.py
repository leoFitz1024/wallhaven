# ===============================================================
def init_frame(self):
    url = QUrl(QFileInfo("page/page_list.html").absoluteFilePath())
    self.online_bg_webwidget.load(url)
    self.online_bg_webwidget.setContextMenuPolicy(Qt.NoContextMenu)
    page = self.online_bg_webwidget.page()
    page.setBackgroundColor(Qt.transparent)
    page.settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)


def bind_event(self):
    """绑定事件"""
    self.my_bg_list.setCurrentRow(0)
    self.my_bg_list.itemClicked.connect(self.my_bg_list_change)
    self.more_info_list.itemClicked.connect(self.more_info_list_change)


def my_bg_list_change(self):
    """侧边栏壁纸监听"""
    self.more_info_list.clearSelection()
    self.contentWidget.setCurrentIndex(self.my_bg_list.currentRow())


def more_info_list_change(self):
    """侧边栏更多监听"""
    self.my_bg_list.clearSelection()
    self.contentWidget.setCurrentIndex(3 + self.more_info_list.currentRow())