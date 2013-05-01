# encoding=UTF-8
'''
Created on 2013-4-28
@author: Administrator
'''

RETRY_TIMES = 10
DOWNLOADER_MIDDLEWARES = {'crawler.shc.fe.middlewares.ProxyRetryMiddleWare':450,
                          'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware':None
                           }
