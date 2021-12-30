import _thread
import json
import os
import configparser
from fractions import Fraction
from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler
import lib.image_utils as image_utils
from lib.image_utils import LOGGER
import lib.utils as utils
import lib.win_function as win_function
from lib.Downloader import Downloader

CONFIG_PATH = f'{os.getcwd()}/config.ini'

FULL_FILE_TPL = "full_{0}"

GRAY_COLOR = [(8, 8, 8), (8, 7, 8), (76, 74, 72), (81, 92, 107), (181, 152, 161), (50, 47, 59), (62, 56, 65),
              (34, 32, 46), (48, 47, 75), (47, 47, 53), (168, 168, 189), (71, 72, 76), (178, 187, 190),
              (71, 75, 76), (115, 124, 123)]

RED_COLOR = [(239, 130, 160), (236, 138, 164), (224, 200, 209), (192, 111, 152)]

BLUE_COLOR = [(45, 125, 154), (142, 140, 216), (128, 118, 163), (128, 118, 163), (128, 109, 158),
              (82, 82, 136), (116, 117, 155), (39, 117, 182), (52, 108, 156), (21, 85, 154),
              (36, 116, 181), (47, 144, 185), (92, 179, 204), (26, 148, 188), (99, 187, 208), (34, 162, 195),
              (33, 55, 61), (59, 129, 140), (134, 157, 157), (66, 134, 117), (73, 117, 104), (96, 124, 137),
              (95, 221, 218)]

YELLOW_COLOR = [(192, 147, 91), (192, 147, 91)]

BG_COLORS = [(8, 7, 8), (231, 124, 142), (128, 118, 163), (45, 153, 163), (207, 204, 201)]

PAGE_URL_TPL = "https://wallhaven.cc/search?categories={0}" \
               "&purity={1}&topRange={2}&sorting={3}" \
               "&order=desc"

DEFAULT_DIR = "wallhaven"

TOP_RANGE_MAP = {
    'Last Day': '1d',
    'Last 3 Days': '3d',
    'Last Week': '1w',
    'Last Month': '1M',
    'Last 3 Months': '3M',
    'Last 6 Months': '6M',
    'Last Year': '1y',
}

TOP_RANGE_TUPLE = ("Last Day", "Last 3 Days", "Last Week", "Last Month",
                   "Last 3 Months", "Last 6 Months", "Last Year")

DEFAULT_PATH = os.path.join(os.getenv('APPDATA'), DEFAULT_DIR)


class Wallhaven:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.error_path = False
        self.current_bg_path = None
        self.download_map = {}
        self.is_changing = False
        self.timer = None
        self.schedule_time = 0
        # 图片id列表
        self.images_ids = []
        self.dislike_ids = set([])
        # config
        self.images_dir = DEFAULT_PATH
        self.max_page = 100
        # url config
        self.categories = 0b111
        self.purity = 0b110
        self.top_range = 3
        self.sorting = "Random"
        self.ratios_list = set(["16x9"])

        # cache
        self.total_page = 100
        self.current_page = 1
        self.current_bg_index = -1
        self.current_bg_id = None
        # 加载配置文件
        self.load_config()
        self.init_job()

    def load_config(self):
        """加载配置文件"""
        self.config = configparser.ConfigParser()
        if os.path.exists(CONFIG_PATH):
            self.config.read(CONFIG_PATH, encoding="utf-8")
            if self.config.has_section("cache"):
                if self.config.has_option("cache", "bg_index"):
                    self.current_bg_index = int(self.config.get("cache", "bg_index"))
                if self.config.has_option("cache", "current_page"):
                    self.current_page = int(self.config.get("cache", "current_page"))
                if self.config.has_option("cache", "total_page"):
                    self.total_page = int(self.config.get("cache", "total_page"))
            if self.config.has_section("config"):
                if self.config.has_option("config", "ratios"):
                    self.ratios_list = set(json.loads(self.config.get("config", "ratios")))
                if self.config.has_option("config", "max_page"):
                    self.max_page = int(self.config.get("config", "max_page"))
                if self.config.has_option("config", "schedule_time"):
                    self.schedule_time = int(self.config.get("config", "schedule_time"))
                if self.config.has_option("config", "categories"):
                    self.categories = int(self.config.get("config", "categories"), 2)
                if self.config.has_option("config", "purity"):
                    self.purity = int(self.config.get("config", "purity"), 2)
                if self.config.has_option("config", "sorting"):
                    self.sorting = self.config.get("config", "sorting")
                if self.config.has_option("config", "top_range"):
                    self.top_range = int(self.config.get("config", "top_range"))
                if self.config.has_option("config", "image_dir"):
                    self.images_dir = self.config.get("config", "image_dir")
                    if not utils.is_pathname_valid(self.images_dir):
                        self.error_path = True
                        self.images_dir = DEFAULT_PATH
                    else:
                        self.error_path = False
            if self.config.has_section("data"):
                if self.config.has_option("data", "image_ids"):
                    self.images_ids = json.loads(self.config.get("data", "image_ids"))
                if self.config.has_option("data", "dislike_ids"):
                    self.dislike_ids = set(json.loads(self.config.get("data", "dislike_ids")))

    def init_job(self):
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
        if len(self.images_ids) == 0:
            self.init_image_ids()
        self.change_bg()
        self.do_schedule_time()
        self.save_config()

    def save_config(self):
        if not self.config.has_section("cache"):
            self.config.add_section("cache")
        if not self.config.has_section("config"):
            self.config.add_section("config")
        if not self.config.has_section("data"):
            self.config.add_section("data")
        self.config.set("cache", "bg_index", str(self.current_bg_index))
        self.config.set("cache", "current_page", str(self.current_page))
        self.config.set("cache", "total_page", str(self.total_page))
        self.config.set("config", "ratios", "[%s]" % ", ".join(map(lambda e: '"%s"' % e, self.ratios_list)))
        self.config.set("config", "max_page", str(self.max_page))
        self.config.set("config", "schedule_time", str(self.schedule_time))
        self.config.set("config", "categories", '{:03b}'.format(self.categories))
        self.config.set("config", "purity", '{:03b}'.format(self.purity))
        self.config.set("config", "sorting", self.sorting)
        self.config.set("config", "top_range", str(self.top_range))
        self.config.set("config", "image_dir", self.images_dir)
        self.config.set("data", "image_ids", "[%s]" % ", ".join(map(lambda e: '"%s"' % e, self.images_ids)))
        self.config.set("data", "dislike_ids", "[%s]" % ", ".join(map(lambda e: '"%s"' % e, self.dislike_ids)))
        self.config.write(open(CONFIG_PATH, "w", encoding="UTF-8"))

    def init_image_ids(self):
        """在线获取图片id"""
        LOGGER.info("init images ids")
        self.images_ids.clear()
        img_id_list, total_page = image_utils.get_images_list(self.format_url(), 1, 2)
        self.total_page = total_page
        self.images_ids.extend(img_id_list)
        win_function.del_duplication(self.images_ids, self.dislike_ids)
        self.current_page = 1
        self.current_bg_index = 0
        self.save_config()
        LOGGER.info("init images ids success")

    def change_bg(self):
        """更新壁纸"""
        if self.current_bg_index != -1 and len(self.images_ids) > 0 \
                and self.current_bg_index < len(self.images_ids):
            self.current_bg_id = self.images_ids[self.current_bg_index]
            self.current_bg_id = self.download_current_bg()
            _thread.start_new_thread(self.del_and_down, ())
            # 图片还在下载等待下载完成
            while self.current_bg_id in self.download_map.keys():
                sleep(0.5)
            # self.full_img(self.current_bg_id)
            bg_color, model = self.get_color_and_model()
            LOGGER.info("current bg:" + self.current_bg_id)
            win_function.set_wall_paper(self.current_bg_path, bg_color, model)
            self.is_changing = False
            self.save_config()

    def download_current_bg(self):
        """下载当前壁纸"""
        img_id = self.images_ids[self.current_bg_index]
        self.current_bg_path = os.path.join(self.images_dir, img_id)
        # 下载图片
        if not os.path.exists(self.current_bg_path):
            downloader = Downloader(LOGGER)
            downloader.download(img_id, self.images_dir)
            while not downloader.finished:
                sleep(0.5)
            if downloader.download_404:
                self.images_ids.remove(img_id)
                self.save_config()
                self.get_next_index()
                return self.download_current_bg()
        return img_id

    def do_schedule_time(self):
        self.save_config()
        if self.schedule_time != 0:
            if self.timer is None:
                self.timer = BackgroundScheduler(timezone='Asia/Shanghai')
            else:
                self.timer.remove_job('schedule_change')
            # 采用非阻塞的方式
            self.timer.add_job(lambda: self.next_bg(), 'interval',
                               seconds=self.schedule_time, id='schedule_change')
            if self.timer.state == 0:
                self.timer.start()
        else:
            LOGGER.info("close timer")
            if self.timer is not None:
                self.timer.remove_job('schedule_change')
                self.timer.shutdown()
                self.timer = None

    def del_and_down(self):
        """下载前后得图片，删除前后间隔超过1的图片"""
        # 下载
        img_id = self.images_ids[self.current_bg_index]
        pre_one = self.current_bg_index - 1 if self.current_bg_index - 1 >= 0 else len(self.images_ids) - 1
        self.thread_download(self.images_ids[pre_one])
        next_one = self.current_bg_index + 1 if self.current_bg_index + 1 < len(self.images_ids) else 0
        self.thread_download(self.images_ids[next_one])

        # 删除图片
        pre_two = self.current_bg_index - 2 if self.current_bg_index - 2 >= 0 \
            else len(self.images_ids) - 2 if self.current_bg_index == 0 else len(self.images_ids) - 1
        self.delete_img(self.images_ids[pre_two])
        next_two = self.current_bg_index + 2 if self.current_bg_index + 2 < len(self.images_ids) \
            else 0 if self.current_bg_index + 2 == len(self.images_ids) else 1
        self.delete_img(self.images_ids[next_two])

    def delete_img(self, img_id):
        del_path = os.path.join(self.images_dir,
                                img_id)
        if img_id in self.download_map.keys():
            self.download_map[img_id].cancel()
            del self.download_map[img_id]
        else:
            if os.path.exists(del_path):
                os.remove(del_path)

    def thread_download(self, img_id):
        """线程下载"""
        if not os.path.exists(
                os.path.join(self.images_dir, img_id)):
            if img_id not in self.download_map.keys():
                downloader = Downloader(LOGGER)
                self.download_map[img_id] = downloader
                downloader.download(img_id, self.images_dir)
                while not downloader.finished:
                    sleep(1)
                if downloader.download_404:
                    self.images_ids.remove(img_id)
                    self.save_config()
                if img_id in self.download_map.keys():
                    del self.download_map[img_id]

    def format_url(self):
        top_range = TOP_RANGE_MAP[TOP_RANGE_TUPLE[self.top_range]]
        sorting_value = self.sorting.lower().replace(' ', '_')
        url = PAGE_URL_TPL.format('{:03b}'.format(self.categories), '{:03b}'.format(self.purity), top_range,
                                  sorting_value)
        if len(self.ratios_list) > 0:
            url = f"{url}&ratios={','.join(self.ratios_list)}"
        return url

    def get_color_and_model(self):
        """取图片主要颜色和定义好的颜色列表比较，取最接近的颜色"""
        try:
            colors, image_size = win_function.get_dominant_colors(self.current_bg_path)
            iw, ih = image_size
            dominant_color = colors[0]
            model = 10
            bg_color = (8, 8, 8)
            if win_function.like_black(dominant_color) or (ih > iw and Fraction(ih, iw) >= Fraction(17, 14)):
                model = 6
                bg_color = win_function.min_color_diff(dominant_color, BG_COLORS)
            return bg_color, model
        except OSError as e:
            if "file is truncated" in str(e):
                LOGGER.info("文件已损坏：" + self.current_bg_path)
                if os.path.exists(self.current_bg_path):
                    os.remove(self.current_bg_path)
                    self.current_bg_id = self.download_current_bg()
                    return self.get_color_and_model()
            else:
                raise e

    def dislike_current(self):
        """不喜欢当前壁纸 加入黑名单"""
        self.dislike_ids.add(self.current_bg_id)
        self.images_ids.remove(self.current_bg_id)
        self.next_bg()

    def last_bg(self):
        if not self.is_changing:
            self.is_changing = True
            _thread.start_new_thread(self.do_last_bg, ())

    def do_last_bg(self):
        self.get_last_index()
        self.change_bg()

    def get_last_index(self):
        """获取上一个壁纸下标"""
        if len(self.images_ids) > 0:
            if self.current_bg_index - 1 > 0:
                self.current_bg_index = self.current_bg_index - 1
            else:
                self.current_bg_index = len(self.images_ids) - 1
        else:
            self.init_image_ids()

    def next_bg(self):
        """下一张"""
        # self.del_temp_img(self.images_ids[self.current_bg_index])
        if not self.is_changing:
            self.is_changing = True
            _thread.start_new_thread(self.do_next_bg, ())

    def do_next_bg(self):
        self.get_next_index()
        self.change_bg()

    def get_next_index(self):
        """获取下一个壁纸下标"""
        if len(self.images_ids) > 0:
            if self.current_bg_index + 1 < len(self.images_ids):
                self.current_bg_index = self.current_bg_index + 1
            elif self.current_page <= self.max_page and self.current_page <= self.total_page:
                """还有下一页且未超过用户设定最大页数 下载下一页图片id"""
                self.get_next_page()
                self.current_bg_index = self.current_bg_index + 1
            else:
                self.current_bg_index = 0
        else:
            self.init_image_ids()

    def get_next_page(self):
        """还有下一页且未超过用户设定最大页数 下载下一页图片id"""
        if self.current_page <= self.max_page and self.current_page <= self.total_page:
            img_id_list, total_page = image_utils.get_images_list(self.format_url(), self.current_page + 1,
                                                                  self.current_page + 2)
            self.total_page = total_page
            self.images_ids.extend(img_id_list)
            win_function.del_duplication(self.images_ids, self.dislike_ids)
            self.current_page += 1
            self.save_config()
