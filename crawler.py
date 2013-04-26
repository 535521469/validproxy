# encoding=utf8
'''
Created on 2013-4-26
@author: corleone
'''
from bot.config import configdata
from const import ValidProxySpiderConst
from multiprocessing.process import Process
from scrapy.crawler import CrawlerProcess
from scrapy.settings import CrawlerSettings
from scrapy.settings.deprecated import check_deprecated_settings
from scrapy.utils.project import get_project_settings
from vp.spiders import SOSOSpider
import sys
import time

class DomainCrawlerScript():
    def __init__(self):
        
        values = configdata[ValidProxySpiderConst.vpsettings]
        settings = CrawlerSettings(values=values)
        
        # --- backwards compatibility for scrapy.conf.settings singleton ---
        if settings is None and 'scrapy.conf' in sys.modules:
            from scrapy import conf
            if hasattr(conf, 'settings'):
                settings = conf.settings
        # ------------------------------------------------------------------
    
        if settings is None:
            settings = get_project_settings()
        check_deprecated_settings(settings)
    
        # --- backwards compatibility for scrapy.conf.settings singleton ---
        import warnings
        from scrapy.exceptions import ScrapyDeprecationWarning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ScrapyDeprecationWarning)
            from scrapy import conf
            conf.settings = settings
        # ------------------------------------------------------------------
    
        self.crawler = CrawlerProcess(settings)
        self.crawler.install()
        self.crawler.configure()
    def _crawl(self, proxies):
        self.crawler.crawl(SOSOSpider(proxies=proxies))
        self.crawler.start()
#        self.crawler.stop()
    def crawl(self, proxies):
#        p = Process(target=self._crawl, args=proxies)
#        p.start()
#        p.join()
        self._crawl(proxies)

crawler = DomainCrawlerScript()

def domain_crawl(proxies):
    crawler.crawl(proxies)
