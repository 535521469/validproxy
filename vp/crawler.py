##encoding=utf8
#'''
#Created on 2013-4-26
#@author: corleone
#'''
#
#from multiprocessing import Process
#from scrapy.crawler import CrawlerProcess
#from scrapy.conf import settings
#from spider import DomainSpider
#from models import Domain
#
#class DomainCrawlerScript():
#    def __init__(self):
#        self.crawler = CrawlerProcess(settings)
#        self.crawler.install()
#        self.crawler.configure()
#    def _crawl(self, domain_pk):
#        urls = []
#        for page domain.pages.all():
#            urls.append(page.url())
#        self.crawler.crawl(DomainSpider(urls))
#        self.crawler.start()
#        self.crawler.stop()
#    def crawl(self, domain_pk):
#        p = Process(target=self._crawl, args=[domain_pk])
#        p.start()
#        p.join()
#
#crawler = DomainCrawlerScript()
#
#def domain_crawl(domain_pk):
#    crawler.crawl(domain_pk)
