# -*- coding: utf-8 -*-
import time
import os
from enum import Enum


class LogUtil:
    def __init__(self, model='console'):
        self.model = model
        if not os.path.exists(f'{os.getcwd()}/log'):
            os.mkdir(f'{os.getcwd()}/log')
        self.log = open(f'{os.getcwd()}/log/%s.txt' % time.strftime("%Y_%m_%d"), 'w+')
        log_files = os.listdir(f'{os.getcwd()}/log/')
        log_files.sort()
        if len(log_files) > 200:
            print('log file >200,delete old file', log_files.pop(0), file=self.log)

    def info(self, *data):
        msg = time.strftime("%Y-%m-%d_%I:%M:%S") + " INFO:"
        for info in data:
            if type(info) == int:
                msg = msg + str(info)
            else:
                msg = msg + str(info)
        self.write_log(msg)

    def warn(self, *data):
        msg = time.strftime("%Y-%M-%d_%I:%M:%S") + " WARN:"
        for info in data:
            if type(info) == int:
                msg = msg + str(info)
            else:
                msg = msg + info
        self.write_log(msg)

    def error(self, *data):
        msg = time.strftime("%Y-%M-%d_%I:%M:%S") + " ERROR:"
        for info in data:
            if type(info) == int:
                msg = msg + str(info)
            else:
                msg = msg + info
        self.write_log(msg)

    def write_log(self, msg):
        if self.model == LOG_MODEL.console:
            print(msg)
        if self.model == LOG_MODEL.file:
            print(msg, file=self.log)
        self.log.flush()


class LOG_MODEL(Enum):
    console = 1
    file = 2
