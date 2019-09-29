import os
import re

import pickle

from typing import Iterable

from agent_spider.config import CACHE_FILENAME


class URLCacheManager:
    RE_URL_ID = re.compile(
        r"onliner\.by\/(?P<type>[a-z]+)\/apartments\/(?P<id>\d+)"
    )

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

    def __key_for_url(self, url):
        """
        https://r.onliner.by/ak/apartments/436768 -> r:436768
        """
        match = self.RE_URL_ID.search(url).groupdict()
        return f"{match['type']}:{match['id']}"

    def dump_cache(self) -> None:
        with open(self.cache_filename, 'wb') as cache_file:
            pickle.dump(self.url_set, cache_file)

    def has_url(self, url: str) -> bool:
        return self.__key_for_url(url) in self.url_set

    def add_url(self, url: str) -> None:
        self.url_set.add(self.__key_for_url(url))

    def add_urls(self, urls: Iterable[str]):
        for url in urls:
            self.add_url(self.__key_for_url(url))
