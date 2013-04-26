# encoding=utf8
'''
Created on 2013-4-26
@author: corleone
'''
from scrapy.spider import BaseSpider
from vp.tools import change_proxy_status
from scrapy.http.request import Request

class SOSOSpider(BaseSpider):
    
    name = u'SOSOSpider'
    
    def __init__(self, name=None, *args, **kwargs):
        BaseSpider.__init__(self, *args, **kwargs)
#        self.start_urls = kwargs.get('urls', [])
        self.lst = kwargs.get('lst', [])
        self.proxies = kwargs[u"proxies"]
    
    start_urls = [u'http://www.soso.com/q?w=xcs', ]
    
    def start_requests(self):
        for proxy in self.proxies:
            yield Request(u'http://www.soso.com/q?w=xcs', self.parse,
                           meta={u'proxy':u'%s://%s:%s' % 
                                 (proxy.procotol, proxy.ip, proxy.port)},
                           cookies={u'proxy':proxy}
                           )
    
    @change_proxy_status
    def parse(self, response):
        
        proxy = response.request.cookes[u'proxy']
        if response.body.find(u'id="sInfo"') != -1:
            yield proxy
        
    
