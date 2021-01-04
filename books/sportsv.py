#!/usr/bin/env python
# -*- coding:utf-8 -*-

from base import BaseFeedBook # 继承基类BaseFeedBook
from lib.urlopener import URLOpener # 导入请求URL获取页面内容的模块
from bs4 import BeautifulSoup # 导入BeautifulSoup处理模块

# 返回此脚本定义的类名
def getBook():
    return sportsv

# 继承基类BaseFeedBook
class sportsv(BaseFeedBook):
    # 设定生成电子书的元数据
    title = u'sportsv' # 设定标题
    __author__ = u'sportsv' # 设定作者
    description = u'sportsv' # 设定简介
    language = 'zh-TW' # 设定语言
    deliver_times=[2,10,18] #2:00,10:00,18:00
    oldest_article=28800 #8*60*60
    fulltext_by_readability = False
    keep_only_tags = [
        dict(name='div', class_='article_full'),
    ]
    remove_classes = ['author_card']
    # 指定要提取的包含文章列表的主题页面链接
    # 每个主题是包含主题名和主题页面链接的元组
    feeds = [
        (u'運動視界-籃球', 'https://www.sportsv.net/basketball/feed'),
    ]
