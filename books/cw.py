#!/usr/bin/env python
# -*- coding:utf-8 -*-

from base import BaseFeedBook # 继承基类BaseFeedBook
from lib.urlopener import URLOpener # 导入请求URL获取页面内容的模块
from bs4 import BeautifulSoup # 导入BeautifulSoup处理模块

# 返回此脚本定义的类名
def getBook():
    return cw

# 继承基类BaseFeedBook
class cw(BaseFeedBook):
    # 设定生成电子书的元数据
    title = u'cw' # 设定标题
    __author__ = u'cw' # 设定作者
    description = u'cw' # 设定简介
    language = 'zh-TW' # 设定语言
    deliver_times=[2,10,18] #2:00,10:00,18:00
    oldest_article=28800 #8*60*60
    fulltext_by_readability = False
    keep_only_tags = [
        dict(name='div', class_='article__head'),
        dict(name='div', class_='article__body pt-d-40 pt-m-30 px20'),
    ]
    remove_classes = ['breadcrumb list-reset','article__provideViews my20 mobile','ad text-center ad--300by250 cw__advertising ad--first','article__keyword mb30']
    # 指定要提取的包含文章列表的主题页面链接
    # 每个主题是包含主题名和主题页面链接的元组
    feeds = [
        (u'天下雜誌精選文章', 'https://www.cw.com.tw/RSS/cw_content.xml'),
    ]
