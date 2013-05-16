# encoding=utf8
'''
Created on 2013-4-28
@author: corleone
'''
from bot.const import HTTPProxyValueConst
from bot.dbutil import FetchSession
from const import AppConst
from scrapy import log
from scrapy.contrib.downloadermiddleware.redirect import RedirectMiddleware
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from scrapy.exceptions import IgnoreRequest
from twisted.internet.error import TCPTimedOutError
import datetime

class ProxyValidRetryMiddleWare(RetryMiddleware):

    def __init__(self, settings):
        RetryMiddleware.__init__(self, settings)

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0)
        if isinstance(reason, TCPTimedOutError):
            reason.args = (u'...',)
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

class ValidatorRedirectMiddleWare(RedirectMiddleware):
    '''
    用来判断推广信息的原始url是否已经抓取过。如果抓取的话，就删除此次抓取任务
    但是为了保存时间序列的信息，此去重被弃用
    '''
    def _redirect(self, redirected, request, spider, reason):

        try:
            fs = FetchSession()
            proxy = request.cookies[AppConst.proxy]
            proxy.validflag = HTTPProxyValueConst.validflag_no
            proxy.validdatetime = datetime.datetime.now()
            fs.merge(proxy)
        except Exception as e:
            msg = (u'error redirect mw %s') % str(e)
            spider.log(msg, log.ERROR)
            fs.rollback()
        else:
            msg = (u"redirect , %s 2 %s ") % (redirected.url, request.url)
            spider.log(msg, log.INFO)
            fs.commit()
        finally:
            fs.close()
        raise IgnoreRequest
