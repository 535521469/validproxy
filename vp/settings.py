DOWNLOADER_MIDDLEWARES = {'vp.mw.ProxyValidRetryMiddleWare':450,
                          'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware':None,
                          'vp.mw.ValidatorRedirectMiddleWare':600,
                          'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware':None,
                           }