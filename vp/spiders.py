# encoding=utf8
'''
Created on 2013-4-26
@author: corleone
'''
from bot.const import HTTPProxyValueConst
from const import AppConst
from scrapy.http.request import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from vp.tools import change_proxy_status, fill_valid_urls_2_cookies

class IP136Spider(BaseSpider):
    name = u'IP136Spider'
    valid_url = u'http://wap.ip138.com/'
    
    @fill_valid_urls_2_cookies
    def start_requests(self):
        for proxy in self.settings[AppConst.proxies]:
            yield Request(u'%sip_search.asp?ip='
                          '%s' % (self.valid_url, proxy.ip), self.parse,
                           meta={u'proxy':u'%s://%s:%s' % 
                                 (proxy.procotol, proxy.ip, proxy.port)},
                           cookies={AppConst.proxy:proxy},
                           dont_filter=True,
                           )
    
    @change_proxy_status
    def parse(self, response):
        proxy = response.request.cookies[AppConst.proxy]
#        hxs = HtmlXPathSelector(response)
#        try:
#            ip = hxs.select('//div[@id="ip"]/strong[1]/text()').extract()[0]
#            if ip == proxy.ip:
#                proxy.validflag = HTTPProxyValueConst.validflag_yes
#            else:
#                proxy.validflag = HTTPProxyValueConst.validflag_no
#        except Exception:
#            proxy.validflag = HTTPProxyValueConst.validflag_no
#        else:
        yield proxy

class SOSOSpider(BaseSpider):
    name = u'SOSOSpider'
    
    valid_url = u'http://www.soso.com/q?w=IP%B5%D8%D6%B7'
    
    @fill_valid_urls_2_cookies
    def start_requests(self):
        for proxy in self.settings[AppConst.proxies]:
            yield Request(self.valid_url, self.parse,
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

class SoGouSpider(BaseSpider):
    name = u'SoGouSpider'
    valid_url = u'http://www.sogou.com/web?query=IP%E5%9C%B0%E5%9D%80'
    @fill_valid_urls_2_cookies
    def start_requests(self):
        for proxy in self.settings[AppConst.proxies]:
            yield Request(self.valid_url, self.parse,
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
            ip = hxs.select('//div[@id="ipsearchresult"]/strong[1]/text()').extract()[0]
            if ip.startswith(proxy.ip):
                proxy.validflag = HTTPProxyValueConst.validflag_yes
            else:
                proxy.validflag = HTTPProxyValueConst.validflag_no
        except Exception:
            proxy.validflag = HTTPProxyValueConst.validflag_no
        else:
            yield proxy

class BaiDuSpider(BaseSpider):
    name = u'BaiDuSpider'
    valid_url = u'http://www.baidu.com/s?wd=IP%E5%9C%B0%E5%9D%80'
    @fill_valid_urls_2_cookies
    def start_requests(self):
        for proxy in self.settings[AppConst.proxies]:
            yield Request(self.valid_url, self.parse,
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
            ip = hxs.select('//p[@class="op_ip_detail"]/strong[1]/text()').extract()[0]
            if ip.startswith(proxy.ip):
                proxy.validflag = HTTPProxyValueConst.validflag_yes
            else:
                proxy.validflag = HTTPProxyValueConst.validflag_no
        except Exception:
            proxy.validflag = HTTPProxyValueConst.validflag_no
        else:
            yield proxy
            
url_spider = {SOSOSpider.valid_url:SOSOSpider,
            SoGouSpider.valid_url:SoGouSpider,
            BaiDuSpider.valid_url:BaiDuSpider,
            IP136Spider.valid_url:IP136Spider,
            }

valid_urls = [IP136Spider.valid_url, SOSOSpider.valid_url, BaiDuSpider.valid_url, SoGouSpider.valid_url]
