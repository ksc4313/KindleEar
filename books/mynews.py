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
    return mynews

# 继承基类BaseFeedBook
class mynews(BaseFeedBook):
    # 设定生成电子书的元数据
    title = u'我的新聞' # 设定标题
    __author__ = u'我的新聞' # 设定作者
    description = u'我的新聞. ' # 设定简介
    language = 'zh-TW' # 设定语言
    deliver_times=[2,10,18] #2:00,10:00,18:00
    oldest_article=28800 #8*60*60
    keep_image = True

    # 指定要提取的包含文章列表的主题页面链接
    # 每个主题是包含主题名和主题页面链接的元组
    feeds = [
        (u'The News Lens 關鍵評論網', 'https://feeds.feedburner.com/TheNewsLens?format=xml'),
        (u'商業周刊 當期雜誌開放文章', 'http://cmsapi.businessweekly.com.tw/?CategoryId=efd99109-9e15-422e-97f0-078b21322450&TemplateId=8E19CF43-50E5-4093-B72D-70A912962D55'),
        (u'商周網站 最新文章', 'http://cmsapi.businessweekly.com.tw/?CategoryId=24612ec9-2ac5-4e1f-ab04-310879f89b33&TemplateId=8E19CF43-50E5-4093-B72D-70A912962D55'),
        (u'商周網站 本週熱門排行', 'http://cmsapi.businessweekly.com.tw/?CategoryId=6f061304-ba38-4de9-9960-4e74420e71a0&TemplateId=8E19CF43-50E5-4093-B72D-70A912962D55'),
        (u'公視新聞網', 'https://about.pts.org.tw/rss/XML/newsfeed.xml'),
        (u'MoneyDJ 頭條新聞', 'https://www.moneydj.com/KMDJ/RssCenter.aspx?svc=NR&fno=1&arg=MB010000'),
        (u'BBC Chinese - 主頁', 'https://www.freefullrss.com/feed.php?url=http%3A%2F%2Ffeeds.bbci.co.uk%2Fzhongwen%2Ftrad%2Frss.xml&max=10&links=preserve&exc=&submit=Create+Full+Text+RSS', True),
        (u'運動視界-籃球', 'https://www.sportsv.net/basketball/feed'),
        (u'T客邦', 'https://feeds.feedburner.com/techbang/daily?format=xml'),
        (u'NBA - 最新 - Google 新聞', 'https://news.google.com/rss/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNRFZxZG5nU0JYcG9MVlJYS0FBUAE?hl=zh-TW&gl=TW&ceid=TW:zh-Hant'),
        (u'地球圖輯隊', 'https://www.freefullrss.com/feed.php?url=https%3A%2F%2Fdq.yam.com%2Frss.php&max=10&links=preserve&exc=&submit=Create+Full+Text+RSS', True),
        (u'癮科技 Cool3c', 'https://www.freefullrss.com/feed.php?url=https%3A%2F%2Ffeeds.feedburner.com%2Fcool3c-show%3Fformat%3Dxml&max=10&links=preserve&exc=&submit=Create+Full+Text+RSS', True),
        (u'數位時代 BusinessNext', 'https://www.bnext.com.tw/rss'),
        (u'經理人 Managertoday', 'https://www.freefullrss.com/feed.php?url=https%3A%2F%2Fwww.managertoday.com.tw%2Frss%2F&max=10&links=preserve&exc=&submit=Create+Full+Text+RSS', True),
        (u'端傳媒 Initium Media', 'https://www.freefullrss.com/feed.php?url=https%3A%2F%2Ftheinitium.com%2Fnewsfeed%2F&max=10&links=preserve&exc=&submit=Create+Full+Text+RSS'),
        (u'免費資源網路社群', 'https://feeds.feedburner.com/freegroup/?format=xml', True),
        (u'PTT熱門文章', 'http://rss.disp.cc/PttHot.xml', True),
        (u'華爾街日報中文版', 'https://cn.wsj.com/zh-hant/rss'),
        (u'電腦玩物', 'http://feeds.feedburner.com/playpc?format=xml', True),
        (u'綠角財經筆記', 'https://www.freefullrss.com/feed.php?url=http%3A%2F%2Ffeeds2.feedburner.com%2Fgreenhornfinancefootnote%3Fformat%3Dxml&max=10&links=preserve&exc=&submit=Create+Full+Text+RSS', True),
        (u'天下雜誌精選文章', 'https://www.freefullrss.com/feed.php?url=https%3A%2F%2Fwww.cw.com.tw%2FRSS%2Fcw_content.xml&max=10&links=preserve&exc=&submit=Create+Full+Text+RSS', True),
        (u'遠見雜誌 - 前進的動力', 'https://www.gvm.com.tw/RSS/rss.asp'),
        (u'TechNews 科技新報', 'https://technews.tw/tn-rss/'),
    ]