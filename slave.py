# encoding=utf8
'''
Created on 2013-4-10
@author: corleone
'''
from bot.config import configdata
from bot.const import HTTPProxyValueConst
from bot.dbitem import HTTPProxy
from bot.dbutil import FetchSession, get_proxies
from celery import Celery
from const import ValidProxySpiderConst as const, AppConst
from multiprocessing.process import Process
from scrapy.cmdline import execute
from scrapy.settings import CrawlerSettings
import datetime
import os
import sys

sys.path.append(os.getcwd())

def fetch51freeproxy():
    values = configdata.get(const.vpsettings, {})
    settings = CrawlerSettings(values=values)
    execute(argv=["scrapy", "crawl", "FOSpider" ], settings=settings)

def build_process(target):
    f51fp = Process(target=target, name=target.__name__)
    f51fp.daemon = 1
    f51fp.start()
    return f51fp

def enqueue(target, p_dict):
    if target.__name__ not in p_dict or not p_dict[target.__name__].is_alive():
        p = build_process(target)
        p_dict[target.__name__] = p
    elif p_dict[target.__name__].is_alive():
        pass

class ValidProcess(Process):
    
    def __init__(self, proxies):
        super(ValidProcess, self).__init__()
        self.proxies = proxies

    def run(self):
        if self.proxies:
            values = configdata.get(const.vpsettings, {})
            values[AppConst.proxies] = self.proxies
            values[const.DOWNLOAD_TIMEOUT] = int(values.get(const.DOWNLOAD_TIMEOUT, 5))
            if const.Console in values:
                if values[const.Console] == u'1':# out to console
                    values[const.LOG_FILE] = None
                else:
                    log_dir = values.get(const.LOG_DIR, os.getcwd())
                    if const.LOG_FILE in values:
                        logfile_prefix = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                        log_file = '%s_%s' % (logfile_prefix, values[const.LOG_FILE])
                        values[const.LOG_FILE] = os.sep.join([log_dir , log_file])

            settings = CrawlerSettings(None, values=values)
            execute(argv=["scrapy", "crawl", 'SOSOSpider' ], settings=settings)

celery = Celery('tasks', broker='amqp://guest@192.168.1.118//')

@celery.task
def run(proxy_ids):
    proxies = get_proxies(proxy_ids, d=datetime.date.today())
    p = ValidProcess(proxies)
    p.start()
    p.join()
