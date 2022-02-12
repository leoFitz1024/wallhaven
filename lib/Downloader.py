# ！/usr/bin/python3
# -*- coding: utf-8 -*-
import _thread
import logging
import math
import os
import asyncio
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep
from urllib.request import urlopen, Request

import requests
from PyQt5.QtCore import QObject, pyqtSignal

ua_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57'
}

download_thread_pool = ThreadPoolExecutor(max_workers=5)


class Downloader(QObject):
    finishedSign = pyqtSignal(str)
    canceledSign = pyqtSignal(str)

    def __init__(self, url, small, resolution, dst, filename=None):
        super(Downloader, self).__init__()
        self.url = url
        self.small = small
        self.resolution = resolution
        self.dst = dst
        self.filename = filename
        # =======
        self.logger = logging.getLogger("WallHaven")
        self.process = DownloadProcess(0, 0)
        self.finishedEvent = threading.Event()
        self.finishedEvent.clear()

    def start(self):
        self.process.state = DownloadState.WAITING
        download_thread_pool.submit(self.download)

    def download(self):
        self.process.state = DownloadState.DOWNLOADING
        if self.filename is None:
            self.filename = os.path.basename(self.url)
        self.file_path = os.path.join(self.dst, self.filename)
        self.temp_file_path = f"{self.file_path}.download"

        # 判断大小一致，表示本地文件存在
        if os.path.exists(self.file_path):
            self.logger.info("文件已经存在,无需下载.")
            self.do_finished()
            return os.path.getsize(self.file_path)

        # 获取文件长度
        try:
            req = Request(self.url, headers=ua_headers)
            file_size = int(urlopen(req).info().get('Content-Length', -1))
        except Exception as e:
            self.logger.error(e)
            self.logger.error("错误，访问url: %s 异常" % self.url)
            return False

        # 判断本地文件存在时
        if os.path.exists(self.temp_file_path):
            # 获取文件大小
            first_byte = os.path.getsize(self.temp_file_path)
        else:
            # 初始大小为0
            first_byte = 0

        # 判断大小一致，表示本地文件存在
        if first_byte >= file_size:
            self.logger.info("文件已经存在,无需下载")
            return file_size

        header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
        # pbar = tqdm(
        #     total=file_size, initial=first_byte,
        #     unit='B', unit_scale=True, desc=self.url.split('/')[-1])
        self.process.initial(file_size, first_byte)
        # 访问url进行下载
        req = requests.get(self.url, headers=header, stream=True)
        try:
            with(open(self.temp_file_path, 'ab')) as f:
                for chunk in req.iter_content(chunk_size=1024):
                    if self.process.state == DownloadState.CANCELED \
                            or self.process.state == DownloadState.PAUSED:
                        break
                    if chunk:
                        f.write(chunk)
                        # pbar.update(1024)
                        self.process.update(1024)

            if self.process.state == DownloadState.CANCELED:
                self.del_temp()
            elif self.process.state == DownloadState.PAUSED \
                    or self.process.state == DownloadState.FAILED:
                pass
            else:
                if self.process.bytesReceived < self.process.bytesTotal:
                    self.download()
                else:
                    self.do_finished()
        except Exception as e:
            self.logger.error(e)
            return False

        # pbar.close()
        return True

    def cancel(self):
        """取消下载"""
        if self.process.state != DownloadState.CANCELED \
                and self.process.state != DownloadState.FINISHED:
            self.logger.debug("取消下载")
            self.process.state = DownloadState.CANCELED
            self.canceledSign.emit(self.url)
            self.finishedEvent.set()

    def pause(self):
        """暂停下载"""
        if self.process.state == DownloadState.DOWNLOADING \
                or self.process.state == DownloadState.WAITING:
            self.process.state = DownloadState.PAUSED

    def resume(self):
        if self.process.state == DownloadState.PAUSED:
            self.start()

    def del_temp(self):
        if os.path.exists(self.temp_file_path):
            os.remove(self.temp_file_path)

    def do_finished(self):
        os.rename(self.temp_file_path, self.file_path)
        self.finishedEvent.set()
        self.process.state = DownloadState.FINISHED
        self.finishedSign.emit(self.url)
        self.logger.info(f"下载完成：{self.url}")


class DownloadProcess:
    def __init__(self, bytesTotal=0, bytesReceived=0):
        self.state = DownloadState.INITIAL
        self.last_bytesReceived = bytesReceived
        self.bytesTotal = bytesTotal
        self.bytesReceived = bytesReceived
        self.speed = 0

    def initial(self, bytesTotal, bytesReceived):
        self.state = DownloadState.DOWNLOADING
        self.bytesTotal = bytesTotal
        self.bytesReceived = bytesReceived
        self.start_cal_speed()

    def update(self, bytesReceived):
        self.bytesReceived += bytesReceived

    def start_cal_speed(self):
        _thread.start_new_thread(self.cal_speed, ())

    def cal_speed(self):
        while self.state == DownloadState.DOWNLOADING and self.bytesReceived < self.bytesTotal:
            sleep(1)
            self.speed = (self.bytesReceived - self.last_bytesReceived)
            self.last_bytesReceived = self.bytesReceived


class DownloadState:
    INITIAL = "initial"
    DOWNLOADING = "downloading"
    WAITING = "waiting"
    PAUSED = "paused"
    CANCELED = "canceled"
    FINISHED = "finished"
    FAILED = "failed"


if __name__ == '__main__':
    url = "https://w.wallhaven.cc/full/wq/wallhaven-wqwv76.jpg"
    dst = "C:\\Users\\chen\\Downloads"
    downloader = Downloader(url, dst)
    downloader.start()
    sleep(5)
    downloader.pause()
    sleep(5)
    downloader.resume()
