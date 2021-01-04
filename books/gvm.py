#!/usr/bin/env python
# -*- coding:utf-8 -*-

from base import BaseFeedBook # 继承基类BaseFeedBook
from lib.urlopener import URLOpener # 导入请求URL获取页面内容的模块
from bs4 import BeautifulSoup # 导入BeautifulSoup处理模块

# 返回此脚本定义的类名
def getBook():
    return gvm

# 继承基类BaseFeedBook
class gvm(BaseFeedBook):
    # 设定生成电子书的元数据
    title = u'gvm' # 设定标题
    __author__ = u'gvm' # 设定作者
    description = u'gvm' # 设定简介
    language = 'zh-TW' # 设定语言
    deliver_times=[2,10,18] #2:00,10:00,18:00
    oldest_article=28800 #8*60*60
    fulltext_by_readability = False
    keep_only_tags = [
        dict(name='div', class_='main_conten'),
    ]
    remove_classes = ['article-review','article-features','article-extended','keyWord article-keyword text-center','article-author','extendedReading','floating-share']
    remove_ids = ['marketingChannelsEntry']
    # 指定要提取的包含文章列表的主题页面链接
    # 每个主题是包含主题名和主题页面链接的元组
    feeds = [
        (u'遠見雜誌 - 前進的動力', 'https://www.gvm.com.tw/RSS/rss.asp'),
    ]
