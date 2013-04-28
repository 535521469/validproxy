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
import os

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
        
def run():
    frequence = configdata[AppConst.app_config].get(AppConst.app_config_frequence, 1800)
    frequence = int(frequence)
    while 1:
        proxy_ids = []
        proxies = get_proxies()
        for idx, proxy in enumerate(proxies):
            proxy_ids.append(proxy.seqid)
            if len(proxy_ids) == 2000:
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
