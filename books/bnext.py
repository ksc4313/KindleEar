#!/usr/bin/env python
# -*- coding:utf-8 -*-

from base import BaseFeedBook # 继承基类BaseFeedBook
from lib.urlopener import URLOpener # 导入请求URL获取页面内容的模块
from bs4 import BeautifulSoup # 导入BeautifulSoup处理模块

# 返回此脚本定义的类名
def getBook():
    return bnext

# 继承基类BaseFeedBook
class bnext(BaseFeedBook):
    # 设定生成电子书的元数据
    title = u'bnext' # 设定标题
    __author__ = u'bnext' # 设定作者
    description = u'bnext' # 设定简介
    language = 'zh-TW' # 设定语言
    deliver_times=[2,10,18] #2:00,10:00,18:00
    oldest_article=28800 #8*60*60
    fulltext_by_readability = False
    # 指定要提取的包含文章列表的主题页面链接
    # 每个主题是包含主题名和主题页面链接的元组
    feeds = [
        (u'數位時代 BusinessNext', 'https://www.bnext.com.tw/articles/p/1'),
    ]
    # 设定内容页需要保留的标签
    keep_only_tags = [
        dict(name='div', class_='DynamicComp static htmlview'),
        dict(name='div', class_='head-summary px-8 pt-4 pb-8'),
        dict(name='h1', class_='head-title f24 font-weight-bold my-4'),
    ]

    # 提取每个主题页面下所有文章URL
    def ParseFeedUrls(self):
        urls = [] # 定义一个空的列表用来存放文章元组
        # 循环处理fees中两个主题页面
        for feed in self.feeds:
            # 分别获取元组中主题的名称和链接
            topic, url = feed[0], feed[1]
            # 请求主题链接并获取相应内容
            opener = URLOpener(self.host, timeout=self.timeout)
            result = opener.open(url)
            # 如果请求成功，并且页面内容不为空
            if result.status_code == 200 and result.content:
                # 将页面内容转换成BeatifulSoup对象
                soup = BeautifulSoup(result.content, 'lxml')
                # 找出当前页面文章列表中所有文章条目
                items = soup.find_all(name='div', class_='BG-Box px-4 mb-4')
                # 循环处理每个文章条目
                for item in items:
                    title = item.a.string # 获取文章标题
                    link = item.a.get('href') # 获取文章链接
                    link = BaseFeedBook.urljoin(url, link) # 合成文章链接
                    urls.append((topic, title, link, None)) # 把文章元组加入列表
            # 如果请求失败通知到日志输出中
            else:
                self.log.warn('Fetch article failed(%s):%s' % \
                    (URLOpener.CodeMap(result.status_code), url))
        # 返回提取到的所有文章列表
        return urls
