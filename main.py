# encoding=utf8
'''
Created on 2013-4-10
@author: corleone
'''
from bot.config import configdata
from bot.dbutil import get_proxies
from const import ValidProxySpiderConst as const, AppConst
from multiprocessing.process import Process
from scrapy.cmdline import execute
from scrapy.settings import CrawlerSettings
from vp.spiders import valid_urls
import datetime
import os
import time

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
                    
        values[const.RETRY_TIMES] = len(valid_urls)
        settings = u'vp.settings'
        module_import = __import__(settings, {}, {}, [''])
        
        settings = CrawlerSettings(module_import, values=values)
        execute(argv=["scrapy", "crawl", 'SOSOSpider' ], settings=settings)
        
def run():
    appconfig = configdata.get(AppConst.app_config, {})
    frequence = appconfig.get(AppConst.app_config_frequence, 1800)
    frequence = int(frequence)
    volume_per_time = appconfig.get(AppConst.volumepertime, 1000)
    volume_per_time = int(volume_per_time)
    ps = []
    while 1:
        proxy_ids = []
        proxies = get_proxies(d=datetime.date.today())
        print u'get %s proxies'%len(proxies)
        for idx, proxy in enumerate(proxies):
            proxy_ids.append(proxy)
            if len(proxy_ids) == volume_per_time:
                p = ValidProcess(proxy_ids)
                ps.append(p)
                print u'%s %s start %s' % (datetime.datetime.now(), p.name,len(proxy_ids))
                p.start()
                proxy_ids = []
        else:
            if proxy_ids:
                p = ValidProcess(proxy_ids)
                ps.append(p)
                print u'%s %s start %s' % (datetime.datetime.now(), p.name,len(proxy_ids))
                p.start()
                proxy_ids = []
                
        print u'%s valid proxy .. sleep %s seconds' % (datetime.datetime.now(),
                                                       frequence)
        time.sleep(frequence)
        while ps:
            p = ps.pop()
            try:
                p.terminate()
                print (u'%s terminate one process %s' % (datetime.datetime.now(),
                                                         p.name))
            except :
                pass
            
            
            

if __name__ == '__main__':
    
    run()
