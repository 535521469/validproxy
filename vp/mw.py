# encoding=utf8
'''
Created on 2013-4-28
@author: corleone
'''
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from bot.dbutil import FetchSession
from bot.const import HTTPProxyValueConst
from scrapy import log

class ProxyValidRetryMiddleWare(RetryMiddleware):

    def __init__(self, settings):
        RetryMiddleware.__init__(self, settings)

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0)
        
        proxy = request.cookies.get(u'proxy')
        if proxy:
            fs = FetchSession()
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
