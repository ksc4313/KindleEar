#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#投递相关功能，GAE平台的cron会每个小时调用请求一次Deliver()
#Author: cdhigh <https://github.com/cdhigh>
import os
from collections import defaultdict
from flask import Blueprint, render_template, request, current_app as app
from flask_babel import gettext as _
from ..back_end.db_models import *
from ..base_handler import *
from ..back_end.task_queue_adpt import create_delivery_task

bpDeliver = Blueprint('bpDeliver', __name__)

#判断需要推送哪些书籍
#GAE的cron调度的请求会有一个HTTP标头：X-Appengine-Cron: true
#cron调度的请求不带任何参数，带参数的是高级设置里面的"现在推送"功能发起的
@bpDeliver.route("/deliver")
def Deliver():
    userName = request.args.get('u')
    isGaeCron = request.headers.get('X-Appengine-Cron')
    if not (isGaeCron or (request.args.get('key') == app.config['DELIVERY_KEY'])):
        default_log.warning('Key invalid.')
        return 'Key invalid.'
    
    if userName: #现在投递【测试使用】，不需要判断时间和星期
        id_ = request.args.get('id', '')
        idList = id_.replace('__', ':').split(',') if id_ else []
        return SingleUserDelivery(userName, idList)
    else: #如果不指定userName，说明是定时cron调用
        return MultiUserDelivery()

#判断所有账号所有已订阅书籍，确定哪些需要推送
def MultiUserDelivery():
    bkQueue = defaultdict(list)
    sentCnt = 0
    for user in KeUser.select():
        if not user.cfg('enable_send'):
            continue

        now = user.local_time()
        for book in user.get_booked_recipe():
            #先判断当天是否需要推送
            day = now.day
            weekday = now.weekday()
            userDays = user.send_days
            if not isinstance(book.send_days, dict): #兼容以前版本
                book.send_days = {}
                book.save()
            bookDaysType = book.send_days.get('type')
            bookDays = book.send_days.get('days')
            #如果特定Recipe设定了推送时间，则以这个时间为优先，不再考虑全局设置值
            if bookDaysType and bookDays:
                if (bookDaysType == 'weekday') and (weekday not in bookDays):
                    continue
                elif (bookDaysType == 'date') and (day not in bookDays):
                    continue
            elif userDays and weekday not in userDays: #user.send_days为空也表示每日推送
                continue
                
            #时间判断
            hr = (now.hour + 1) % 24
            bookTimes = book.send_times
            if bookTimes:
                if hr not in bookTimes:
                    continue
            elif user.send_time != hr:
                continue
            
            #到了这里就是需要推送的
            queueOneBook(bkQueue, user, book.recipe_id, book.separated, reason='cron')
            sentCnt += 1
    flushQueueToPush(bkQueue, reason='cron')
    return "Put {} recipes into queue.".format(sentCnt)

#判断指定用户的书籍和订阅哪些需要推送
#userName: 账号名
#idList: recipe id列表，id格式：custom:xx,upload:xx,builtin:xx，为空则推送指定账号下所有订阅
def SingleUserDelivery(userName: str, idList: list=None):
    user = KeUser.get_or_none(KeUser.name == userName)
    if not user or ('email' in user.cfg('delivery_mode') and not user.cfg('kindle_email')):
        return render_template('autoback.html', tips=_('The username does not exist or the email is empty.'))

    #这里不判断特定账号是否已经订阅了指定的书籍，只要提供就推送
    if idList:
        toPush = []
        for id_ in idList:
            recipeType, dbId = Recipe.type_and_id(id_)
            bked = user.get_booked_recipe(id_)
            #如果没有启用自定义RSS推送
            r = Recipe.get_by_id_or_none(dbId) if (not bked and (recipeType == 'custom')) else None
            if r:
                toPush.append({'id_': r.recipe_id, 'separated': r.custom.get('separated', False), 
                    'title': r.title})
            elif bked:
                toPush.append({'id_': bked.recipe_id, 'separated': bked.separated, 'title': bked.title})
    else: #推送特定账号所有订阅的书籍
        toPush = [{'id_': r.recipe_id, 'separated': r.separated, 'title': r.title}
            for r in user.get_booked_recipe()]
    
    sent = []
    bkQueue = defaultdict(list)
    for bked in toPush:
        queueOneBook(bkQueue, user, bked['id_'], bked['separated'], reason='manual')
        sent.append(f'<i>{bked["title"]}</i>')
    flushQueueToPush(bkQueue, reason='manual')
    
    if sent:
        tips = (_("The following recipes has been added to the push queue.") + '<br/>&nbsp;&nbsp;&nbsp;&nbsp;' 
            + '<br/>&nbsp;&nbsp;&nbsp;&nbsp;'.join(sent))
    else:
        tips = _("There are no recipes to deliver.")

    return render_template('autoback.html', tips=tips)

#根据设置，将书籍预先放到队列之后一起推送，或马上单独推送
#queueToPush: 用来缓存的一个字典，用户名为键，元素为recipeId列表
#user: KeUser实例
#recipeId: Recipe Id, custom:xx, upload:xx, builtin:xx
#separated: 是否单独推送
#reason: cron/manual，启动推送的原因
def queueOneBook(queueToPush: defaultdict, user: KeUser, recipeId: str, separated: bool, reason='cron'):
    recipeId = recipeId.replace(':', '__')
    if separated:
        key = os.environ.get('DELIVERY_KEY', '')
        create_delivery_task({'userName': user.name, 'recipeId': recipeId, 'reason': reason, 'key': key})
    else:
        queueToPush[user.name].append(recipeId) #合并推送

#启动推送队列中的书籍
def flushQueueToPush(queueToPush: defaultdict, reason='cron'):
    key = os.environ.get('DELIVERY_KEY', '')
    for name in queueToPush:
        create_delivery_task({'userName': name, 'recipeId': ','.join(queueToPush[name]), 'reason': reason, 'key': key})
    queueToPush.clear()

