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
    return test

# 继承基类BaseFeedBook
class test(BaseFeedBook):
    # 设定生成电子书的元数据
    title = u'test' # 设定标题
    __author__ = u'test' # 设定作者
    description = u'test. ' # 设定简介
    language = 'zh-TW' # 设定语言
    deliver_times=[2,10,18] #2:00,10:00,18:00
    fulltext_by_readability = False
    keep_only_tags = [
        dict(name='div', class_='article-header-container'),
        dict(name='div', class_='article-main-box'),
        dict(name='article', class_='pageContent'),
        dict(name='div', class_='Single-article WebContent'),
    remove_classes = ['Google-special d-md-block']

    # 指定要提取的包含文章列表的主题页面链接
    # 每个主题是包含主题名和主题页面链接的元组
    feeds = [
        (u'The News Lens 關鍵評論網', 'https://feeds.feedburner.com/TheNewsLens?format=xml'),
        (u'商業周刊 當期雜誌開放文章', 'http://cmsapi.businessweekly.com.tw/?CategoryId=efd99109-9e15-422e-97f0-078b21322450&TemplateId=8E19CF43-50E5-4093-B72D-70A912962D55'),
        (u'商周網站 最新文章', 'http://cmsapi.businessweekly.com.tw/?CategoryId=24612ec9-2ac5-4e1f-ab04-310879f89b33&TemplateId=8E19CF43-50E5-4093-B72D-70A912962D55'),
    ]
