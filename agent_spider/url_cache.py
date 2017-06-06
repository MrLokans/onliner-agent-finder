import os

import pickle

from typing import Iterable

from agent_spider.config import CACHE_FILENAME


class URLCacheManager(object):
    def __init__(self, cache_filename: str = CACHE_FILENAME):
        self.cache_filename = cache_filename
        self.url_set = set()

    def load_cache(self) -> None:
        cache_exists = os.path.exists(self.cache_filename)
        cache_is_file = os.path.isfile(self.cache_filename)
        if not cache_exists or not cache_is_file:
            return
        with open(self.cache_filename, 'rb') as f:
            self.url_set = pickle.load(f)

    def dump_cache(self) -> None:
        with open(self.cache_filename, 'wb') as cache_file:
            pickle.dump(self.url_set, cache_file)

    def has_url(self, url: str) -> bool:
        return url in self.url_set

    def add_url(self, url: str) -> None:
        self.url_set.add(url)

    def add_urls(self, urls: Iterable[str]):
        for url in urls:
            self.add_url(url)
