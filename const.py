# encoding=utf8
'''
Created on 2013-4-26
@author: corleone
'''

class ScrapyConst(object):
    BOT_NAME = u'BOT_NAME'
    SPIDER_MODULES = u'SPIDER_MODULES'
    LOG_LEVEL = u'LOG_LEVEL'
    LOG_FILE = u'LOG_FILE'
    LOG_DIR = u'LOG_DIR'
    DOWNLOAD_TIMEOUT = u'DOWNLOAD_TIMEOUT'
    Console = u'Console'
    RETRY_TIMES = u'RETRY_TIMES'

class ValidProxySpiderConst(ScrapyConst):
    vpsettings = u'vpsettings'

class AppConst(object):
    app_config = u'app'
    app_config_frequence = u'frequence'
    proxies = u'proxies'
    proxy = u'proxy'
    volumepertime = u'volume_per_time'
    
    valid_urls = u'valid_urls'
    
