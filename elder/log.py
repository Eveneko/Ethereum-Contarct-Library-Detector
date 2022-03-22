#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging

from .config import *
 
 
class Logger:
    def __init__(self, set_level="INFO",
                 name=os.path.split(os.path.splitext(sys.argv[0])[0])[-1],
                 log_name=time.strftime("%Y-%m-%d.log", time.localtime()),
                 log_path=LOG_PATH,
                 use_console=True):
        """
        :param set_level: 日志级别["NOTSET"|"DEBUG"|"INFO"|"WARNING"|"ERROR"|"CRITICAL"]，默认为INFO
        :param name: 日志中打印的name，默认为运行程序的name
        :param log_name: 日志文件的名字，默认为当前时间（年-月-日.log）
        :param log_path: 日志文件夹的路径，默认为logger.py同级目录中的log文件夹
        :param use_console: 是否在控制台打印，默认为True
        """
        self.__logger = logging.getLogger(name)
        
        # 设置日志级别
        self.setLevel(getattr(logging, set_level.upper()) if hasattr(logging, set_level.upper()) else logging.INFO)
        
        # 创建日志目录
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        handler_list = list()

        fh = logging.FileHandler(os.path.join(log_path, log_name), encoding="utf-8")
        handler_list.append(fh)

        if use_console:
            ch = logging.StreamHandler()
            handler_list.append(ch)
        for handler in handler_list:
            handler.setFormatter(formatter)
            self.addHandler(handler)
 
    def __getattr__(self, item):
        return getattr(self.logger, item)
 
    @property
    def logger(self):
        return self.__logger

logger = Logger()