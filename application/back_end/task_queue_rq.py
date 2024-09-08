#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#任务队列rq
#Author: cdhigh <https://github.com/cdhigh>

#启动rq的worker命令，在shell下执行
#windows: set FLASK_APP=main.py
#linux: export FLASK_APP=main.py
#flask rq worker

from flask_rq2 import RQ

rq = RQ()

def init_task_queue_service(app):
    app.config['RQ_REDIS_URL'] = app.config['TASK_QUEUE_BROKER_URL']
    rq.init_app(app)
    #windows不支持，暂时屏蔽，正式版本需要取消注释, TODO
    #每隔一个小时执行一次
    check_deliver.cron('40 */1 * * *', 'check_deliver') #type:ignore
    #每隔24小时执行一次
    remove_logs.cron('0 0 */1 * *', 'remove_logs') #type:ignore
    return rq

@rq.job
def check_deliver():
    from ..view.deliver import MultiUserDelivery
    MultiUserDelivery()

@rq.job
def remove_logs():
    from ..view.logs import RemoveLogs
    RemoveLogs()

@rq.job
def start_rq_worker_impl(**payload):
    from ..work.worker import WorkerImpl
    return WorkerImpl(**payload)

@rq.job
def start_rq_url2book(**payload):
    from ..work.url2book import Url2BookImpl
    return Url2BookImpl(**payload)

@rq.job
def start_rq_notifynewsubs(**payload):
    from ..view.subscribe import NotifyNewSubscription
    return NotifyNewSubscription(**payload)

def create_delivery_task(payload: dict):
    start_rq_worker_impl.queue(**payload) #type:ignore

def create_url2book_task(payload: dict):
    start_rq_url2book.queue(**payload) #type:ignore

def create_notifynewsubs_task(payload: dict):
    start_rq_notifynewsubs.queue(**payload) #type:ignore
