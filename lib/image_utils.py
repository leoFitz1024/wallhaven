# -*- coding: utf-8 -*-
import math
import os
from fractions import Fraction
import numpy as np
from PIL import Image
from lxml import etree
import requests

from lib.LogUtil import LogUtil, LOG_MODEL

LOGGER = LogUtil(LOG_MODEL.file)

img_url_template = "https://w.wallhaven.cc/full/{0}/wallhaven-{1}.jpg"

ua_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57'
}


def get_images_list(page_url_prefix, start_page, end_page):
    """
    :param page_url_prefix: url 前缀
    :param start_page: wallhaven toplist 开始页
    :param end_page: 页结束页
    """
    LOGGER.info(f"get_images_list:{page_url_prefix}||{start_page},{end_page}")
    img_id_list = []
    total_page = 0
    page_url_template = page_url_prefix + "&page={0}"
    i = start_page
    while i < end_page:
        url = page_url_template.format(i)
        i += 1
        result = requests.get(url, headers=ua_headers, allow_redirects=True)
        # 为防止出错，编码utf-8
        result.encoding = 'utf-8'
        # 将html构建为Xpath模式
        root = etree.HTML(result.content)
        # 使用Xpath语法，获取图片id
        page_figure_list = root.xpath("//section[@class='thumb-listing-page']//ul//li//figure")
        for figure in page_figure_list:
            img_id = figure.xpath("@data-wallpaper-id")[0]
            span_class = figure.xpath(f"//figure[@data-wallpaper-id='{img_id}']//div[@class='thumb-info']/span/@class")
            img_type = 'jpg'
            if len(span_class) > 1:
                img_type = span_class[1]
            img_id_list.append(f"{img_id}.{img_type}")
        pagination = root.xpath("//ul[@class='pagination']//li//a/@original-title")
        total_page = int(pagination[len(pagination) - 1].split(" ")[1])
        if end_page - 1 > total_page:
            end_page = total_page + 1
    return img_id_list, total_page


# 下载图片
def download_images(save_dir, img_id):
    img_url = img_url_template.format(img_id[0:2], img_id)
    img_req = requests.get(img_url, stream=True)
    if img_req.status_code == 200:
        img_file_path = os.path.join(save_dir, "{0}.jpg".format(img_id))
        with open(img_file_path, 'wb') as fd:
            for chunk in img_req.iter_content(4096):
                fd.write(chunk)
            fd.close()
    else:
        LOGGER.info("download error:" + img_id)


# 改变图片大小并填充图片
def pad_image(image, target_size):
    """
    :param image: input image
    :param target_size: a tuple (num,num)
    :return: new image
    """

    iw, ih = image.size  # 原始图像的尺寸
    w, h = target_size  # 目标图像的尺寸

    # print("original size: ", (iw, ih))
    # print("new size: ", (w, h))

    scale = min(w / iw, h / ih)  # 转换的最小比例

    # 保证长或宽，至少一个符合目标图像的尺寸 0.5保证四舍五入
    nw = int(iw * scale + 0.5)
    nh = int(ih * scale + 0.5)

    # print("now nums are: ", (nw, nh))

    image_arr = np.array(image)
    new_img_arr = np.full((h, w, 3), [0, 0, 0])
    for index_h in range(h):
        line_left_color_arr = np.full((w // 2, 3), image_arr[index_h, 2])
        line_right_color_arr = np.full((w // 2, 3), image_arr[index_h, iw - 2])
        line_color_arr = np.insert(line_right_color_arr, 0, values=line_left_color_arr, axis=0)
        if len(line_color_arr) < w:
            line_color_arr = np.append(line_color_arr, [line_right_color_arr[0]], axis=0)
        new_img_arr[index_h] = line_color_arr
    new_image = Image.fromarray(np.uint8(new_img_arr))

    # 为整数除法，计算图像的位置
    new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))  # 将图像填充为中间图像，两侧为黑色的样式
    # new_image.show()
    return new_image


# 填充图像并生成新图片
def full_image(img_path, save_dir, numerator, denominator):
    """
    :param img_path: 原图路径
    :param save_dir: 新图保存路径
    :param denominator: 图片比例的分子
    :param numerator: 图片比例的分母
    """
    fd = open(img_path, 'rb')
    try:
        image = Image.open(fd)
        image_file_name = os.path.basename(img_path)  # 带后缀的文件名
        new_file_name = "{0}_full.{1}".format(image_file_name.split('.')[0], image_file_name.split('.')[1])
        iw, ih = image.size  # 原始图像的尺寸
        # 比例符合 直接返回
        if Fraction(iw / ih) == Fraction(numerator / denominator):
            return img_path
        print("full image：" + image_file_name)
        size = (math.ceil(ih * Fraction(numerator / denominator)), ih)
        new_image = pad_image(image, size)
        new_file_path = os.path.join(save_dir, new_file_name)
        new_image.save(new_file_path)
        return new_file_path
    finally:
        fd.close()


if __name__ == '__main__':
    url = "https://wallhaven.cc/search?categories=111&purity=100&ratios=16x9%2C21x9&sorting=hot&order=desc&topRange=1W"
    get_images_list(url, 1, 2)
