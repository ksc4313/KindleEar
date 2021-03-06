#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re, datetime
import urllib
import json
from bs4 import BeautifulSoup
from lib.urlopener import URLOpener
from base import BaseFeedBook

# 返回此脚本定义的类名
def getBook():
    return nbanews

# 继承基类BaseFeedBook
class nbanews(BaseFeedBook):
    # 设定生成电子书的元数据
    title = u'nbanews' # 设定标题
    __author__ = u'nbanews' # 设定作者
    description = u'nbanews. ' # 设定简介
    language = 'zh-TW' # 设定语言
    deliver_times=[2,10,18] #2:00,10:00,18:00
    oldest_article=28800 #8*60*60
    keep_image = True

    # 指定要提取的包含文章列表的主题页面链接
    # 每个主题是包含主题名和主题页面链接的元组
    feeds = [
        (u'NBA - 最新 - Google 新聞', 'https://news.google.com/rss/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNRFZxZG5nU0JYcG9MVlJYS0FBUAE?hl=zh-TW&gl=TW&ceid=TW:zh-Hant'),
    ]
