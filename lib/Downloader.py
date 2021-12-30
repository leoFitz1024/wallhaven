# coding=utf-8
import os
import threading
from time import sleep
import requests

img_url_template = "https://w.wallhaven.cc/full/{0}/wallhaven-{1}"

ua_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57'
}


class Downloader:

    def __init__(self, logger):
        self.LOGGER = logger
        self.stop_down = False
        self.thread = None
        self.finished = False
        self.download_404 = False

    def download(self, img_id, save_dir):
        self.thread = threading.Thread(target=self.__down, args=(img_id, save_dir))
        self.thread.start()

    def __down(self, img_id, save_dir):
        img_url = img_url_template.format(img_id[0:2], img_id)
        img_req = requests.get(img_url, stream=True)
        self.LOGGER.info("download:" + img_url)
        if img_req.status_code == 200:
            img_file_path = os.path.join(save_dir, img_id)
            with open(img_file_path, 'wb') as fd:
                for chunk in img_req.iter_content(8192):
                    if self.stop_down:
                        self.LOGGER.info("stop download:" + img_url)
                        break
                    fd.write(chunk)
                fd.close()
            if self.stop_down and os.path.exists(img_file_path):
                os.remove(img_file_path)
        elif img_req.status_code == 404:
            self.LOGGER.error("404 error:{0} url:{1}".format(img_id, img_url))
            self.download_404 = True
        else:
            self.LOGGER.error("download error:{0} url:{1}".format(img_id, img_url))
        self.finished = True

    def cancel(self):
        self.stop_down = True


if __name__ == '__main__':
    url = 'https://w.wallhaven.cc/full/j3/wallhaven-j3l79p.jpg'
    d = Downloader()
    d.download(url, './images/wallhaven-j3l79p.jpg')
    sleep(1)
    d.cancel()
    # while True:
    #     pass
