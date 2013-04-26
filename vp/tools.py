# encoding =utf8
'''
Created on 2013-4-26
@author: corleone
'''
from functools import wraps
from bot.dbitem import HTTPProxy
from bot.dbutil import FetchSession
from bot.const import HTTPProxyValueConst
from scrapy import log

def change_proxy_status(parse):
    @wraps
    def simulate_parse(self, response):
        for rs in parse(self, response):
            if isinstance(rs, HTTPProxy):
                fs = FetchSession()
                try:
                    rs.validflag = HTTPProxyValueConst.validflag_yes
                    fs.merge(rs)
                except Exception as e:
                    self.log(u'change_proxy_status error %s' % str(e),
                             log.CRITICAL)
                    fs.rollback()
                else:
                    self.log(u'pass valid %s://%s:%s' % 
                             (rs.procotol, rs.ip, rs.port), log.INFO)
                    fs.commit()
                finally:
                    fs.close()
    return simulate_parse
