# encoding=utf8
'''
Created on 2013-4-10
@author: corleone
'''
from bot.config import configdata
from bot.const import HTTPProxyValueConst
from bot.dbitem import HTTPProxy
from bot.dbutil import FetchSession
from const import ValidProxySpiderConst as const, AppConst
from multiprocessing.process import Process
from scrapy.cmdline import execute
from scrapy.settings import CrawlerSettings
import datetime
import time

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

def get_proxies():
    fs = FetchSession()
    try:
        status = [HTTPProxyValueConst.validflag_yes,
                  HTTPProxyValueConst.validflag_null, ]
        proxies = fs.query(HTTPProxy).filter(HTTPProxy.validflag.in_(status)).all()
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
        values = configdata.get(const.vpsettings, {})
        values[AppConst.proxies] = self.proxies
        values[const.DOWNLOAD_TIMEOUT] = int(values.get(const.DOWNLOAD_TIMEOUT, 5))
        logfile_prefix = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        values[const.LOG_FILE] = '%s_%s' % (logfile_prefix,
                                         values[const.LOG_FILE])
        settings = CrawlerSettings(None, values=values)
        execute(argv=["scrapy", "crawl", 'SOSOSpider' ], settings=settings)
        
def run():
    frequence = configdata[AppConst.app_config].get(AppConst.app_config_frequence, 1800)
    frequence = int(frequence)
    while 1:
        proxy_ids = []
        proxies = get_proxies()
        for idx, proxy in enumerate(proxies):
            proxy_ids.append(proxy.seqid)
            if len(proxy_ids) == 500:
                p = ValidProcess(proxies)
                p.start()
                proxy_ids = []
        else:
            if proxy_ids:
                p = ValidProcess(proxies)
                p.start()
                
        time.sleep(frequence)

if __name__ == '__main__':
    
    run()
