import logging
import requests
import os
from enum import Enum
import random
import string
import time


class Purity(Enum):
    sfw = "sfw"
    sketchy = "sketchy"
    nsfw = "nsfw"


class Category(Enum):
    general = "general"
    anime = "anime"
    people = "people"


class Sorting(Enum):
    date_added = "date_added"
    relevance = "relevance"
    random = "random"
    views = "views"
    favorites = "favorites"
    toplist = "toplist"


class Order(Enum):
    # desc used by default
    desc = "desc"
    asc = "asc"


class TopRange(Enum):
    one_day = "1d"
    three_days = "3d"
    one_week = "1w"
    one_month = "1M"
    three_months = "3M"
    six_months = "6M"
    one_year = "1y"


class Color(Enum):
    # Color names from http://chir.ag/projects/name-that-color
    lonestar = "660000"
    red_berry = "990000"
    guardsman_red = "cc0000"
    persian_red = "cc3333"
    french_rose = "ea4c88"
    plum = "993399"
    royal_purple = "663399"
    sapphire = "333399"
    science_blue = "0066cc"
    pacific_blue = "0099cc"
    downy = "66cccc"
    atlantis = "77cc33"
    limeade = "669900"
    verdun_green = "336600"
    verdun_green_2 = "666600"
    olive = "999900"
    earls_green = "cccc33"
    yellow = "ffff00"
    sunglow = "ffcc33"
    orange_peel = "ff9900"
    blaze_orange = "ff6600"
    tuscany = "cc6633"
    potters_clay = "996633"
    nutmeg_wood_finish = "663300"
    black = "000000"
    dusty_gray = "999999"
    silver = "cccccc"
    white = "ffffff"
    gun_powder = "424153"


class Type(Enum):
    jpeg = "jpeg"
    jpg = "jpg"  # the same as jpeg
    png = "png"


class Seed(object):
    @staticmethod
    def generate():
        # [a-zA-Z0-9]{6}
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


class RequestsLimitError(Exception):
    def __init__(self):
        super().__init__("You have exceeded requests limit. Please try later.")


class ApiKeyError(Exception):
    def __init__(self):
        super().__init__("Bad api key. Check it please.")


class UnhandledException(Exception):
    def __init__(self):
        super().__init__("Somthing went wrong. Please submit this issue to "
                         "https://github.com/Goblenus/WallhavenApi/issues.")


class NoWallpaperError(Exception):
    def __init__(self, wallpaper_id):
        super().__init__("No wallpaper with id {}".format(wallpaper_id))


class WallhavenApiV1:
    def __init__(self, api_key=None, verify_connection=True, base_url="https://wallhaven.cc/api/v1",
                 timeout=(2, 5), requestslimit_timeout=None, proxies={}):
        self.verify_connection = verify_connection
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.requestslimit_timeout = requestslimit_timeout
        self.proxies = proxies

    def set_api_key(self, api_key):
        self.api_key = api_key
        try:
            self.my_collections()
        except ApiKeyError:
            self.api_key = None
            return False
        return True

    def request(self, to_json, **kwargs):
        for i in range(self.requestslimit_timeout[0] if self.requestslimit_timeout is not None else 1):
            if self.api_key is not None:
                if "params" in kwargs:
                    kwargs["params"]["apikey"] = self.api_key
                else:
                    kwargs["params"] = {"apikey": self.api_key}

            if "timeout" not in kwargs:
                kwargs["timeout"] = self.timeout

            if "verify" not in kwargs:
                kwargs["verify"] = self.verify_connection

            if "proxies" not in kwargs:
                kwargs["proxies"] = self.proxies

            response = requests.request(**kwargs)

            if response.status_code == 429:
                if self.requestslimit_timeout is None \
                   or i == (self.requestslimit_timeout[0] - 1) if self.requestslimit_timeout is not None else 0:
                    raise RequestsLimitError

                time.sleep(self.requestslimit_timeout[1])
                continue

            if response.status_code == 401:
                raise ApiKeyError

            if response.status_code != 200:
                raise UnhandledException

            if to_json:
                try:
                    return response.json()
                except:
                    raise UnhandledException

            return response

    def url_format(self, *args):
        url = self.base_url
        url += "/" if not url.endswith("/") else ""

        return url + "/".join((str(x) for x in args))

    @staticmethod
    def _category(general=True, anime=True, people=False):
        return "{}{}{}".format(int(general), int(anime), int(people))

    @staticmethod
    def _purity(sfw=True, sketchy=True, nsfw=False):
        return "{}{}{}".format(int(sfw), int(sketchy), int(nsfw))

    def search(self, q=None, categories=None, purities=None, sorting=None, order=None, top_range=None, atleast=None,
               resolutions=None, ratios=None, colors=None, page=None, seed=None):
        params = {}
        if q is not None:
            params["q"] = q

        if categories is not None:
            categories = categories if type(categories) is list else [categories]
            params["categories"] = self._category(Category.general in categories, Category.anime in categories,
                                                  Category.people in categories)

        if purities is not None:
            purities = purities if type(purities) is list else [purities]
            params["purity"] = self._purity(Purity.sfw in purities, Purity.sketchy in purities,
                                            Purity.nsfw in purities)

        if sorting is not None:
            params["sorting"] = sorting.value

        if order is not None:
            params["order"] = order.value

        if top_range is not None:
            params["topRange"] = top_range.value

        if atleast is not None:
            params["atleast"] = "{}x{}".format(atleast[0], atleast[1])

        if resolutions is not None:
            params["resolutions"] = ",".join(["{}x{}".format(x[0], x[1]) \
                                              for x in (resolutions if type(resolutions) is list else [resolutions])])

        if ratios is not None:
            params["ratios"] = ",".join(["{}x{}".format(x[0], x[1]) \
                                         for x in (ratios if type(ratios) is list else [ratios])])

        if colors is not None:
            params["colors"] = colors.value

        if page is not None:
            params["page"] = str(page)

        if seed is not None:
            params["seed"] = seed

        return self.request(True, method="get", url=self.url_format("search"), params=params)

    def wallpaper(self, wallpaper_id):
        return self.request(True, method="get", url=self.url_format("w", wallpaper_id))

    def is_walpaper_exists(self, wallpaper_id):
        return "error" not in self.wallpaper(wallpaper_id)

    def download_walpaper(self, *args, **kwargs):
        logging.warning('Please use "download_wallpaper" method instead "download_walpaper"')
        return self.download_wallpaper(*args, **kwargs)

    def download_wallpaper(self, wallpaper_id, file_path, chunk_size=4096):
        wallpaper_data = self.wallpaper(wallpaper_id)

        if "error" in wallpaper_data:
            raise NoWallpaperError(wallpaper_id)

        wallpaper = requests.get(wallpaper_data["data"]["path"], stream=True, timeout=self.timeout,
                                 verify=self.verify_connection)

        if wallpaper.status_code != 200:
            raise UnhandledException

        if file_path is not None:
            save_path = os.path.abspath(file_path)
            save_directory_path = os.path.dirname(save_path)

            if not os.path.exists(save_directory_path):
                os.makedirs(save_directory_path)

            with open(save_path, "wb") as image_file:
                for chunk in wallpaper.iter_content(chunk_size):
                    image_file.write(chunk)

            return save_path

        return wallpaper.content

    def tag(self, tag_id):
        return self.request(True, method="get", url=self.url_format("tag", tag_id))

    def settings(self):
        return None if self.api_key is None else self.request(True, method="get", url=self.url_format("settings"))

    def collections(self, user_name):
        return self.request(True, method="get", url=self.url_format(f"collections/{user_name}"))

    def collection_wallpapers(self, user_name, collection_id, page=None):
        return self.request(True, method="get", url=self.url_format(f"collections/{user_name}/{collection_id}"),
                             params={"page": str(page)} if page is not None else {})

    def my_collections(self):
        return None if self.api_key is None else self.request(True, method="get", url=self.url_format(f"collections"))
