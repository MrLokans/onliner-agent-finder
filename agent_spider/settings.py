ITEM_PIPELINES = {
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 50,
}
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPCACHE_EXPIRATION_SECS = 20 * 60
HTTPCACHE_ENABLED = True
LOG_LEVEL = 'INFO'
