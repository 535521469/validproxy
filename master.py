# encoding=utf8
'''
Created on 2013-4-27
@author: corleone
'''
from bot.config import configdata
from const import AppConst
from slave import get_proxies, run
import time

frequence = configdata[AppConst.app_config].get(AppConst.app_config_frequence, 1800)
frequence = int(frequence)

proxy_ids = []
proxies = get_proxies()
for idx, proxy in enumerate(proxies):
    proxy_ids.append(proxy.seqid)
    if len(proxy_ids) == 100:
        run.delay(proxy_ids)
        proxy_ids = []
else:
    if proxy_ids:
        run.delay(proxy_ids)
    
    print u'sleep %s seconds' % frequence
    time.sleep(frequence)
