#!/usr/bin/env python
# -*- coding:utf-8 -*-

from base import BaseFeedBook # 继承基类BaseFeedBook

# 返回此脚本定义的类名
def getBook():
    return ChinaDaily

# 继承基类BaseFeedBook
class ChinaDaily(BaseFeedBook):
    # 设定生成电子书的元数据
    title = u'The News Lens 關鍵評論網' # 设定标题
    __author__ = u'The News Lens 關鍵評論網' # 设定作者
    description = u'The News Lens 關鍵評論網. ' # 设定简介
    language = 'zh-TW' # 设定语言
    deliver_times=[6,14,22] #6:00,14:00,22:00
    oldest_article=28800 #8*60*60

    # 指定要提取的包含文章列表的主题页面链接
    # 每个主题是包含主题名和主题页面链接的元组
    feeds = [
        (u'The News Lens 關鍵評論網', 'https://feeds.feedburner.com/TheNewsLens?format=xml'),
    ]
