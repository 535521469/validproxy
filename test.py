from bot.config import configdata
from const import ValidProxySpiderConst, AppConst
from scrapy.cmdline import execute
from scrapy.settings import CrawlerSettings
from start import get_proxies

proxies = get_proxies()
values = configdata.get(ValidProxySpiderConst.vpsettings, {})
values[AppConst.proxies] = proxies
#settings = CrawlerSettings(None, values=values)

settings = u'vp.settings'
module_import = __import__(settings, {}, {}, [''])
settings = CrawlerSettings(module_import, values=values)

execute(argv=["scrapy", "crawl", 'SOSOSpider' ], settings=settings)