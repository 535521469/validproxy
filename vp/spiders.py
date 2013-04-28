# encoding=utf8
'''
Created on 2013-4-26
@author: corleone
'''
from scrapy.spider import BaseSpider
from vp.tools import change_proxy_status
from scrapy.http.request import Request
from scrapy.selector import HtmlXPathSelector
from bot.const import HTTPProxyValueConst
from const import AppConst

class SOSOSpider(BaseSpider):
    name = u'SOSOSpider'
    
    def start_requests(self):
        for proxy in self.settings[AppConst.proxies]:
            yield Request(u'http://www.soso.com/q?w=IP%B5%D8%D6%B7', self.parse,
                           meta={u'proxy':u'%s://%s:%s' % 
                                 (proxy.procotol, proxy.ip, proxy.port)},
                           cookies={AppConst.proxy:proxy},
                           dont_filter=True,
                           )
    
    @change_proxy_status
    def parse(self, response):
        proxy = response.request.cookies[AppConst.proxy]
        hxs = HtmlXPathSelector(response)
        try:
            ip = hxs.select('//div[@id="ip"]/strong[1]/text()').extract()[0]
            if ip == proxy.ip:
                proxy.validflag = HTTPProxyValueConst.validflag_yes
            else:
                proxy.validflag = HTTPProxyValueConst.validflag_no
        except Exception:
            proxy.validflag = HTTPProxyValueConst.validflag_no
        else:
            yield proxy
            


        
