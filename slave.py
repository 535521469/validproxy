# encoding=utf8
'''
Created on 2013-4-10
@author: corleone
'''
from bot.config import configdata
from bot.const import HTTPProxyValueConst
from bot.dbitem import HTTPProxy
from bot.dbutil import FetchSession
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

def get_proxies(proxy_ids=None):
    fs = FetchSession()
    try:
        status = [HTTPProxyValueConst.validflag_yes,
                  HTTPProxyValueConst.validflag_null, ]
        proxies = fs.query(HTTPProxy).filter(HTTPProxy.validflag.in_(status))
        if proxy_ids:
            proxies = proxies.filter(HTTPProxy.seqid.in_(proxy_ids))
        proxies = proxies.all()
        return proxies
    except Exception as e:
        print str(e)
        fs.rollback()
        raise e
    else:
        fs.commit()
    finally:
        fs.close()

class ValidProcess(Process):
    
    def __init__(self, proxies):
        super(ValidProcess, self).__init__()
        self.proxies = proxies

    def run(self):
        if self.proxies:
            values = configdata.get(const.vpsettings, {})
            values[AppConst.proxies] = self.proxies
            values[const.DOWNLOAD_TIMEOUT] = int(values.get(const.DOWNLOAD_TIMEOUT, 5))
            logfile_prefix = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            values[u'LOG_FILE'] = '%s_%s' % (logfile_prefix,
                                             values[const.LOG_FILE])
            settings = CrawlerSettings(None, values=values)
            execute(argv=["scrapy", "crawl", 'SOSOSpider' ], settings=settings)

celery = Celery('tasks', broker='amqp://guest@192.168.1.118//')

@celery.task
def run(proxy_ids):
    proxies = get_proxies(proxy_ids)
    p = ValidProcess(proxies)
    p.start()
    p.join()