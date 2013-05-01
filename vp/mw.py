# encoding=utf8
'''
Created on 2013-4-28
@author: corleone
'''
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from const import AppConst
from bot.dbutil import FetchSession
from bot.const import HTTPProxyValueConst
from scrapy import log
from vp.spiders import url_spider, valid_urls

class ProxyValidRetryMiddleWare(RetryMiddleware):

    def __init__(self, settings):
        RetryMiddleware.__init__(self, settings)

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0)
        if retries <= self.max_retry_times - 1:
            self.priority_adjust = 1
            retryreq = request.copy()
            valie_urls = request.cookies.get(AppConst.valid_urls, [])
            try:
                next_valid_url = valid_urls.pop()
            except Exception:
                pass
            else:
                retryreq = retryreq.replace(callback=url_spider.get(next_valid_url)().parse)    
                retryreq = retryreq.replace(url=next_valid_url)    
            
            return retryreq
        else:
            fs = FetchSession()
            proxy = request.cookies.get(AppConst.proxy)
            try:
                proxy.validflag = HTTPProxyValueConst.validflag_no
                fs.merge(proxy)
            except Exception as _:
                fs.rollback()
            else:
                msg = (u'{proxy.procotol}://{proxy.ip}:{proxy.port} fail for '
                       '{reason.__class__.__name__}'.format(**locals()))
                spider.log(msg, log.INFO)
                fs.commit()
            finally:
                fs.close()
