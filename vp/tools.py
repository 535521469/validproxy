# encoding =utf8
'''
Created on 2013-4-26
@author: corleone
'''
from bot.dbitem import HTTPProxy
from bot.dbutil import FetchSession
from scrapy import log
from functools import wraps

def change_proxy_status(parse):
    @wraps(parse)
    def simulate_parse(self, response):
        rss = parse(self, response)
        if rss:
            for rs in rss:
                if isinstance(rs, HTTPProxy):
                    fs = FetchSession()
                    try:
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
