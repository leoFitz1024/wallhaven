"""
1、启动，启动browser
2、接收配置信息请求写入内存
{
    api_params: 请求参数
    api_key: apikey
    schedule_time: 定时时间
    download_dir: 下载路径
    current_page: 当前页（缓存当前页图片文件名，最大页数）
    page_index: 当前页index
    total_page: 最大页数
    switch_model:online,local 轮换模式
    download_list:下载列表
    auto_start:是否开机自启
    full_model: 图片适配模式
    bg_color: 背景色
    local_bg_index: 本地轮换index
}
3、加载不喜欢列表
4、下载图片，使用browser的下载，请求，保存downloadItem到内存中，定时发送下载进度信息，下载完成发送下载完成。
5、下一张、上：
    文件夹模式：缓存标志false，苏区下载路径下所有文件路径到内存 true，直接设置壁纸
    在线模式：缓存去当页index ++ ==length-1&&page <= totalPage 获取下一页 否之下一页不可用，
6、设置壁纸功能
7、定时切换
"""
import ctypes
import logging

import win32api
import win32con
import win32gui
import _thread
import json
import os
from threading import Thread

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers import interval
import win32com.client as client

from lib.Browser import Browser
from lib.Downloader import Downloader, DownloadState
from lib.HttpServer import HttpServer
from lib.WebBridge import WebBridge
from lib.wallhavenapi import WallhavenApiV1

# os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = "9223"
BG_MODEL = [(10, 0), (6, 0), (2, 0), (0, 1), (0, 0), (22, 0)]
"""
填充
适应
拉伸
平铺
居中
跨区
"""


class WallhavenV2(QMainWindow):
    IMG_FILE_TYPE = (".png", ".jpeg", ".jpg", ".bmp", ".gif")

    def __init__(self, *args, **kwargs):
        super(WallhavenV2, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger("WallHaven")
        self.wallhaven_api = WallhavenApiV1(verify_connection=True,
                                            base_url="http://wallhaven.cc/api/v1",
                                            requestslimit_timeout=(15, 5))
        self.current_bg_file_path = ''
        self.is_changing = False
        self.desktop_width = win32api.GetSystemMetrics(0)
        self.desktop_height = win32api.GetSystemMetrics(1)
        self.page_data = []
        self.dislike_ids = set([])
        self.scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
        self.localStorage = {}
        self.download_map = {}
        self.http_server = HttpServer(self)
        http_server_thread = Thread(target=self.http_server.start, args=[])
        http_server_thread.setDaemon(True)
        http_server_thread.start()
        # self.load_config()

    """=====================ui start==========================="""

    def init_path(self, exe_path, abs_path):
        self.ABSPATH = abs_path
        self.DEFAULT_IMAGES_PATH = f'{self.ABSPATH}\\wallpaper\\'
        self.EXE_PATH = exe_path

    def setIcon(self, trayIcon):
        self.setWindowIcon(trayIcon.my_icon)
        self.trayIcon = trayIcon

    def setupUi(self):
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
        self.retranslateUi()
        # 去菜单栏
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.load_web()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Wallhaven v2.0"))

    def load_web(self):
        # 禁用右键
        self.browser.setContextMenuPolicy(Qt.NoContextMenu)
        self.page = self.browser.page()
        # 禁用滚动条
        self.page.settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
        # 清除缓存
        # self.page.profile().clearHttpCache()
        self.logger.debug(self.page.profile().persistentStoragePath())
        # os.remove(self.page.profile().persistentStoragePath())
        self.page.setBackgroundColor(Qt.transparent)
        self.webBridge = WebBridge()
        self.webBridge.SigSelectFolder.connect(self.select_image_folder)
        self.webBridge.SigOpenFolder.connect(self.open_folder)
        self.webBridge.windowMaximized.connect(self.showMaximized)
        self.webBridge.windowMinimized.connect(self.showMinimized)
        self.webBridge.windowClosed.connect(self.close)
        self.pWebChannel = QWebChannel()
        self.pWebChannel.registerObject("webBridge", self.webBridge)
        self.page.setWebChannel(self.pWebChannel)
        self.page.settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
        url = QUrl("http://localhost:1746/index.html#/online")
        self.browser.load(url)

    """======================ui end=========================="""

    def open_folder(self, path):
        os.startfile(path)

    def select_image_folder(self, path):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹", self.localStorage['download_dir'])
        if folder != "":
            self.webBridge.SigImgFolderChanged.emit(folder)

    # def load_config(self):
    #     """加载配置文件"""
    #     self.config = configparser.ConfigParser()
    #     if os.path.exists(WallhavenV2.CONFIG_PATH):
    #         self.config.read(WallhavenV2.CONFIG_PATH, encoding="utf-8")
    #         if self.config.has_section("data"):
    #             if self.config.has_option("data", "dislike_ids"):
    #                 self.dislike_ids = set(json.loads(self.config.get("data", "dislike_ids")))

    def dislike_current(self):
        if os.path.exists(self.current_bg_file_path):
            os.remove(self.current_bg_file_path)
        self.next_bg()

    def next_bg(self):
        """下一张"""
        if not self.is_changing:
            if self.localStorage['switch_model'] == 'online':
                if (self.localStorage['page_index'] < len(self.page_data) - 1) or (
                        self.localStorage['current_page'] < self.localStorage['total_page']):
                    self.is_changing = True
                    _thread.start_new_thread(self.do_online_next_bg, ())
            else:
                _thread.start_new_thread(self.do_local_next_bg, ())

    def last_bg(self):
        if not self.is_changing:
            if self.localStorage['switch_model'] == 'online':
                if (0 < self.localStorage['page_index'] < len(self.page_data)) or (
                        1 < self.localStorage['current_page'] <= self.localStorage['total_page']):
                    self.is_changing = True
                    _thread.start_new_thread(self.do_online_last_bg, ())
            else:
                _thread.start_new_thread(self.do_local_lase_bg, ())

    def do_online_next_bg(self):
        if self.localStorage['page_index'] < len(self.page_data) - 1:
            self.localStorage['page_index'] += 1
        else:
            self.localStorage['page_index'] = 0
            self.localStorage['current_page'] += 1
            self.update_page_data()
        current_img_info = self.page_data[self.localStorage['page_index']]
        if self.download_image(current_img_info):
            self.do_change_bg()
        else:
            self.is_changing = False

    def do_online_last_bg(self):
        if self.localStorage['page_index'] > 0:
            self.localStorage['page_index'] -= 1
        else:
            self.localStorage['current_page'] -= 1
            self.update_page_data()
            self.localStorage['page_index'] = len(self.page_data) - 1
        current_img_info = self.page_data[self.localStorage['page_index']]
        if self.download_image(current_img_info):
            self.do_change_bg()
        else:
            self.is_changing = False

    def do_local_next_bg(self):
        for root, dirs, files in os.walk(self.localStorage['download_dir']):
            images = [i for i in files if i.endswith(WallhavenV2.IMG_FILE_TYPE)]
            if len(images) > 0:
                self.localStorage['local_bg_index'] += 1
                if self.localStorage['local_bg_index'] >= len(images):
                    self.localStorage['local_bg_index'] = 0
                self.current_bg_file_path = os.path.join(self.localStorage['download_dir'],
                                                         images[self.localStorage['local_bg_index']])
                self.do_change_bg()

    def do_local_last_bg(self):
        for root, dirs, files in os.walk(self.localStorage['download_dir']):
            images = [i for i in files if i.endswith(WallhavenV2.IMG_FILE_TYPE)]
            if len(images) > 0:
                self.localStorage['local_bg_index'] -= 1
                if self.localStorage['local_bg_index'] >= len(images) or self.localStorage['local_bg_index'] == 0:
                    self.localStorage['local_bg_index'] = len(images) - 1
                self.current_bg_file_path = os.path.join(self.localStorage['download_dir'],
                                                         images[self.localStorage['local_bg_index']])
                self.do_change_bg()

    def update_page_data(self):
        url = f"""{self.wallhaven_api.url_format("search")}?{self.localStorage['api_params']}&page={self.localStorage['current_page']}"""
        self.logger.debug(url)
        response = self.wallhaven_api.request(True, method="get",
                                              url=url,
                                              params={})
        if self.localStorage['total_page'] > response['meta']['last_page']:
            self.localStorage['current_page'] = 1
            self.localStorage['total_page'] = response['meta']['last_page']
            self.update_page_data()
        else:
            self.localStorage['total_page'] = response['meta']['last_page']
        self.page_data.clear()
        for img_item in response['data']:
            item = {
                'path': img_item['path'],
                'colors': img_item['colors'],
                'small': img_item['thumbs']['small'],
                'resolution': img_item['resolution']
            }
            self.page_data.append(item)
        self.check_icon_menu()

    def check_icon_menu(self):
        if self.localStorage['current_page'] == 1 \
                and self.localStorage['page_index'] == 0:
            self.trayIcon.last.setEnabled(False)
        else:
            self.trayIcon.last.setEnabled(True)

        if self.localStorage['current_page'] == self.localStorage['total_page'] \
                and self.localStorage['page_index'] == len(self.page_data) - 1:
            self.trayIcon.next.setEnabled(False)
        else:
            self.trayIcon.next.setEnabled(True)

    def set_bg(self, img_info):
        if "small" not in img_info.keys():
            self.current_bg_file_path = img_info['path']
        else:
            url = img_info['path']
            filename = os.path.basename(url)
            file_path = os.path.join(self.localStorage['download_dir'], filename)
            if not os.path.exists(file_path):
                _thread.start_new_thread(self.delay_change, (img_info, file_path))
                return "downloading"
            else:
                self.current_bg_file_path = file_path
        self.do_change_bg()
        return "success"

    def delay_change(self, img_info, file_path):
        self.download_image(img_info)
        self.current_bg_file_path = file_path
        self.do_change_bg()

    def download_image(self, img_info):
        try:
            url = img_info['path']
            filename = os.path.basename(url)
            self.current_bg_file_path = os.path.join(self.localStorage['download_dir'], filename)
            if not os.path.exists(self.current_bg_file_path):
                downloader = self.download(url, img_info['small'], img_info['resolution'],
                                           self.localStorage['download_dir'])
                if isinstance(downloader, Downloader):
                    downloader.finishedEvent.wait()
                    if downloader.process.state == DownloadState.FINISHED:
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                return True
        except Exception as e:
            self.logger.error(e)
            return False

    def do_change_bg(self):
        """
            :param pic: 图片路径
            :param bg_color: 颜色RGB值 tuple (122, 122, 122)
            :param model:
                0填充
                1适应
                2拉伸
                3平铺
                4居中
                5跨区
            :return:
        """
        bg_color_str = self.localStorage['bg_color'].replace("rgb(", "")
        bg_color_str = bg_color_str.replace(")", "")
        bg_color_str_arr = bg_color_str.split(",")
        bg_color = (int(bg_color_str_arr[0]), int(bg_color_str_arr[1]), int(bg_color_str_arr[2]))
        model = self.localStorage['full_model']
        try:
            self.logger.info("切换壁纸:" + self.current_bg_file_path)
            # return
            pic = self.current_bg_file_path
            # open register
            regKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0,
                                           win32con.KEY_SET_VALUE)
            regKey2 = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Colors", 0,
                                            win32con.KEY_SET_VALUE)
            # 设置填充风格
            win32api.RegSetValueEx(regKey, "WallpaperStyle", 0, win32con.REG_SZ, str(BG_MODEL[model][0]))
            win32api.RegSetValueEx(regKey, "TileWallpaper", 0, win32con.REG_SZ, str(BG_MODEL[model][1]))
            # 设置背景色
            r, g, b = bg_color
            color = win32api.RGB(r, g, b)
            win32api.RegSetValueEx(regKey2, "Background", 0, win32con.REG_SZ, "%d %d %d" % bg_color)
            ctypes.windll.user32.SetSysColors(1, ctypes.byref(ctypes.c_int(1)), ctypes.byref(ctypes.c_int(color)))
            # 设置图片
            win32api.RegSetValueEx(regKey, "WallPaper", 0, win32con.REG_SZ, pic)
            # refresh screen
            win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, pic, win32con.SPIF_SENDWININICHANGE)
            self.is_changing = False
            pageInfo = {
                "current_page": self.localStorage['current_page'],
                "page_index": self.localStorage['page_index'],
                "local_bg_index": self.localStorage['local_bg_index'],
            }
            self.webBridge.SigUpdatePageInfo.emit(json.dumps(pageInfo))
            self.check_icon_menu()
        except Exception as e:
            self.logger.error(e)

    def download(self, url, small, resolution, dst=None, filename=None):
        # url = "http://mirrors.aliyun.com/centos/7/isos/x86_64/CentOS-7-x86_64-Everything-2009.iso"
        self.logger.info(f"download:{url}")
        filename = os.path.basename(url)
        if dst is None:
            dst = self.localStorage['download_dir']
        path = os.path.join(dst, filename)
        if not os.path.exists(path):
            if url in self.download_map.keys():
                return self.download_map[url]
            else:
                downloader = Downloader(url, small, resolution, dst, filename)
                self.download_map[url] = downloader
                download_infos = [{
                    "url": url,
                    "small": small,
                    "resolution": resolution
                }]
                self.webBridge.SigAddDownloadTask.emit(json.dumps(download_infos))
                downloader.start()
                downloader.finishedSign.connect(self.finished_download_call)
                downloader.canceledSign.connect(self.cancel_download_call)
                return downloader
        else:
            return "file exist"

    def finished_download_call(self, url):
        downloadItem = self.download_map.pop(url)
        info = {
            "url": downloadItem.url,
            "small": downloadItem.small,
            "resolution": downloadItem.resolution,
            "bytesTotal": downloadItem.process.bytesTotal
        }
        self.webBridge.SigDownloadFinished.emit(json.dumps(info))

    def cancel_download_call(self, url):
        self.download_map.pop(url)
        self.webBridge.SigDownloadCanceled.emit(url)

    def load_download_task(self):
        """从缓存加载下载任务"""
        for item in self.localStorage["downloadList"].values():
            downloader = Downloader(item['url'], item['small'], item['resolution'], self.localStorage['download_dir'])
            downloader.process.state = DownloadState.PAUSED
            downloader.finishedSign.connect(self.finished_download_call)
            downloader.canceledSign.connect(self.cancel_download_call)
            self.download_map[item['url']] = downloader

    def load_scheduler(self):
        schedule_time = self.localStorage["schedule_time"] * 60
        if self.localStorage["schedule_time"] != 0:
            self.scheduler.remove_all_jobs()
            trigger = interval.IntervalTrigger(seconds=schedule_time, timezone="Asia/Shanghai")
            self.scheduler.add_job(lambda: self.next_bg(), trigger=trigger, id='schedule_change',
                                   replace_existing=True)
            if self.scheduler.state == 0:
                self.scheduler.start()
        else:
            if self.scheduler is not None and self.scheduler.state != 0:
                self.scheduler.remove_all_jobs()
                self.scheduler.shutdown()

    def load_auto_run(self):
        name = 'wallhaven'  # 要添加的项值名称
        path = f""""{self.EXE_PATH}" AutoRun"""  # 要添加的exe路径
        # 注册表项名
        KeyName = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
        if self.localStorage['auto_start'] == 1:
            # 异常处理
            try:
                win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, path)
                self.logger.debug('添加成功！')
            except Exception as e:
                self.logger.error(e)
                self.logger.error('添加失败')
            finally:
                win32api.RegCloseKey(key)
        else:
            try:
                win32api.RegDeleteValue(key, name)
            except Exception as e:
                if "系统找不到指定的文件。" not in str(e):
                    self.logger.error(e)
                    self.logger.error('删除失败')
            finally:
                win32api.RegCloseKey(key)

    def load_auto_run_by_link(self):
        name = 'Wallhaven'  # 快捷方式名称
        path = self.EXE_PATH  # 要添加的exe路径
        # 设置快捷方式的起始位置，此处设置为windows启动目录
        working_directory = os.getenv(
            'USERPROFILE') + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
        link_path = os.path.join(working_directory, name + '.lnk')
        if self.localStorage['auto_start'] == 1:
            if not os.path.exists(link_path):
                try:
                    self.createShortCut(working_directory, path, name)
                    self.logger.info("开机自启：ON")
                except Exception as e:
                    self.logger.error(e.args)
        else:
            if os.path.exists(link_path):
                os.remove(link_path)
            self.logger.info("开机自启：OFF")

    def createShortCut(self, save_path, target_path, link_name):
        # 创建快捷方式的目标绝对路径
        link_path = os.path.join(save_path, link_name + '.lnk')
        # 要创建快捷方式的文件的绝对路径，此处是获取当前路径
        shortcut = client.Dispatch("WScript.Shell").CreateShortCut(link_path)
        shortcut.TargetPath = target_path
        shortcut.Arguments = " AutoRun"
        shortcut.save()
        self.logger.debug('创建快捷方式')

    # ==============接口方法=====================
    def init_images_dir(self):
        if not os.path.exists(self.localStorage['download_dir']):
            os.makedirs(self.localStorage['download_dir'])

    def start_exe(self, json_data):
        """接口方法 缓存参数"""
        self.localStorage = json_data
        res_info = "success"
        # print(self.localStorage)
        if self.localStorage['download_dir'] == "":
            self.localStorage['download_dir'] = self.DEFAULT_IMAGES_PATH
            res_info = "set_download_dir"
        if self.localStorage['api_key'] is not None and self.localStorage['api_key'] != '':
            self.wallhaven_api.set_api_key(self.localStorage['api_key'])
        self.init_images_dir()
        self.load_download_task()
        self.load_scheduler()
        self.load_auto_run_by_link()
        self.update_page_data()
        res = {
            "info": res_info,
            "desktopInfo": f"{self.desktop_width} x {self.desktop_height}",
            "data": self.localStorage
        }
        return res

    def wallhaven_request(self, url):
        return self.wallhaven_api.request(False, url=url, method="get", params={})

    def get_download_list(self):
        """接口方法 返回下载列表"""
        download_list = []
        for downloadItem in self.download_map.values():
            finishedRatio = 0 if downloadItem.process.bytesTotal == 0 else round(
                downloadItem.process.bytesReceived / downloadItem.process.bytesTotal, 6) * 100
            download_list.append({
                "url": downloadItem.url,
                "small": downloadItem.small,
                "resolution": downloadItem.resolution,
                "state": downloadItem.process.state,
                "bytesTotal": downloadItem.process.bytesTotal,
                "bytesReceived": downloadItem.process.bytesReceived,
                "speed": downloadItem.process.speed,
                "finishedRatio": finishedRatio
            })
        return download_list

    def cancel_download(self, url):
        downloader = self.download_map[url]
        if downloader is not None:
            downloader.cancel()
            return True
        else:
            return False

    def pause_download(self, url):
        downloader = self.download_map[url]
        if downloader is not None:
            downloader.pause()
            return True
        else:
            return False

    def resume_download(self, url):
        downloader = self.download_map[url]
        if downloader is not None:
            downloader.resume()
            return True
        else:
            return False

    def save_config(self, config):
        old_full_model = self.localStorage['full_model']
        old_schedule_time = self.localStorage['schedule_time']
        old_auto_run = self.localStorage['auto_start']

        if config['api_key'] == '' or self.wallhaven_api.set_api_key(config['api_key']):
            self.localStorage['api_key'] = config['api_key']
            self.localStorage['schedule_time'] = config['schedule_time']
            self.localStorage['download_dir'] = config['download_dir']
            self.localStorage['switch_model'] = config['switch_model']
            self.localStorage['full_model'] = config['full_model']
            self.localStorage['auto_start'] = config['auto_start']
            self.localStorage['bg_color'] = config['bg_color']
            if not self.is_changing and old_full_model != self.localStorage['full_model']:
                self.do_change_bg()
            if old_schedule_time != self.localStorage['schedule_time']:
                self.load_scheduler()
            if old_auto_run != self.localStorage['auto_start']:
                self.load_auto_run_by_link()
            return "success"
        else:
            return "api key error"

# ==============接口方法 end=====================
