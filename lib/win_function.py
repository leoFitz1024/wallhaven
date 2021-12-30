#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ctypes
from colorsys import rgb_to_hsv

from PIL import Image

import win32api
import win32con
import win32gui


# 设置壁纸
def set_wall_paper(pic, bg_color, model):
    """
    :param pic: 图片路径
    :param bg_color: 颜色RGB值 tuple (122, 122, 122)
    :param model: 2：拉伸  0：居中  6：适应  10：填充
    :return:
    """

    # open register
    regKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    regKey2 = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Colors", 0, win32con.KEY_SET_VALUE)
    # 设置填充风格
    win32api.RegSetValueEx(regKey, "WallpaperStyle", 0, win32con.REG_SZ, str(model))
    win32api.RegSetValueEx(regKey, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # 设置背景色
    r, g, b = bg_color
    color = win32api.RGB(r, g, b)
    win32api.RegSetValueEx(regKey2, "Background", 0, win32con.REG_SZ, "%d %d %d" % bg_color)
    ctypes.windll.user32.SetSysColors(1, ctypes.byref(ctypes.c_int(1)), ctypes.byref(ctypes.c_int(color)))
    # 设置图片
    win32api.RegSetValueEx(regKey, "WallPaper", 0, win32con.REG_SZ, pic)
    # refresh screen
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, pic, win32con.SPIF_SENDWININICHANGE)


def get_dominant_colors(in_file):
    fd = open(in_file, 'rb')
    try:
        """获取颜色列表 同时返回size"""
        image = Image.open(fd)
        image_size = image.size
        small_image = image.resize((100, 100))
        result = small_image.convert(
            "P", palette=Image.ADAPTIVE, colors=10
        )  # image with only 10 dominating colors

        # Find dominant colors
        palette = result.getpalette()
        color_counts = sorted(result.getcolors(), reverse=True)
        colors = list()

        for i in range(10):
            palette_index = color_counts[i][1]
            dominant_color = palette[palette_index * 3: palette_index * 3 + 3]
            colors.append(tuple(dominant_color))
        return colors, image_size
    finally:
        fd.close()


def to_hsv(color):
    """ converts color tuples to floats and then to hsv """
    return rgb_to_hsv(*[x / 255.0 for x in color])  # rgb_to_hsv wants floats!


def color_dist(c1, c2):
    """ returns the squared euklidian distance between two color vectors in hsv space """
    return sum((a - b) ** 2 for a, b in zip(to_hsv(c1), to_hsv(c2)))


def min_color_diff(source_color, colors):
    """ returns the `(distance, color_name)` with the minimal distance to `colors`"""

    target_color = min((color_dist(source_color, test), test)  # (distance to `test` color, color name)
                       for test in colors)[1]
    return target_color


def like_black(color):
    """判断颜色是否接近黑色"""
    if color[0] < 12 and \
            color[1] < 12 and \
            color[2] < 12 and \
            abs(color[0] - color[1]) < 8 and \
            abs(color[1] - color[2]) < 8 and \
            abs(color[0] - color[2]) < 8:
        return True
    else:
        return False


def del_duplication(_list, _set):
    """list 中去除 set"""
    for item in _set:
        if item in _list:
            _list.remove(item)
