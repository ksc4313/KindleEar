#!/usr/bin/env python
# -*- coding:utf-8 -*-

from base import BaseFeedBook # 继承基类BaseFeedBook
from lib.urlopener import URLOpener # 导入请求URL获取页面内容的模块
from bs4 import BeautifulSoup # 导入BeautifulSoup处理模块

# 返回此脚本定义的类名
def getBook():
    return wsj

# 继承基类BaseFeedBook
class wsj(BaseFeedBook):
    # 设定生成电子书的元数据
    title = u'wsj' # 设定标题
    __author__ = u'wsj' # 设定作者
    description = u'wsj' # 设定简介
    language = 'zh-TW' # 设定语言
    deliver_times=[2,10,18] #2:00,10:00,18:00
    oldest_article=28800 #8*60*60
    fulltext_by_readability = False
    keep_only_tags = [
        dict(name='div', class_='wsj-article-headline-wrap'),
        dict(name='div', class_='module'),
    ]
    # 指定要提取的包含文章列表的主题页面链接
    # 每个主题是包含主题名和主题页面链接的元组
    feeds = [
        (u'華爾街日報中文版', 'https://cn.wsj.com/zh-hant/rss'),
    ]
    needs_subscription = True
    login_url = 'https://sso.accounts.dowjones.com/login?state=g6Fo2SBsOXJiVEs0Y2VzSlA1UTRnd0dCMkU4bllEVk9ua3R1RKN0aWTZIDVuQjVFVHJmUy1RMG5xNWNUVnRkSEJWTmpnc082Qlkxo2NpZNkgNWhzc0VBZE15MG1KVElDbkpOdkM5VFhFdzNWYTdqZk8&client=5hssEAdMy0mJTICnJNvC9TXEw3Va7jfO&protocol=oauth2&scope=openid%20idp_id%20roles%20email%20given_name%20family_name%20djid%20djUsername%20djStatus%20trackid%20tags%20prts%20suuid&response_type=code&redirect_uri=https%3A%2F%2Faccounts.wsj.com%2Fauth%2Fsso%2Flogin&nonce=14764b8b-baeb-41c5-a1fb-56878284fa48&ui_locales=zh-cn-x-cwsj-19-2&ns=prod%2Faccounts-wsj&savelogin=on#!/signin'
    account = 'libacq@nccu.edu.tw'
    password = 'ncculib2018'
