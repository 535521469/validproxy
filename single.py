# encoding=UTF-8
'''
Created on 2013-4-28

@author: Administrator
'''
from bot.config import configdata
from bot.dbutil import get_proxies
from const import ValidProxySpiderConst as const, AppConst
from scrapy.cmdline import execute
from scrapy.settings import CrawlerSettings
from vp.spiders import valid_urls
import datetime
import os

class ValidProcess(object):
    
    def __init__(self, proxies):
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
                    
        values[const.RETRY_TIMES] = len(valid_urls)
        settings = u'vp.settings'
        module_import = __import__(settings, {}, {}, [''])
        
        settings = CrawlerSettings(module_import, values=values)
        execute(argv=["scrapy", "crawl", 'SOSOSpider' ], settings=settings)
        
if __name__ == '__main__':
    
    proxies = get_proxies(d=datetime.date.today())
    
    ValidProcess(proxies).run()
