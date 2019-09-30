import os
import re

import pickle

from typing import Iterable

from agent_spider.config import CACHE_FILENAME


RE_URL_ID = re.compile(
    r"onliner\.by\/(?P<type>[a-z]+)\/apartments\/(?P<id>\d+)"
)


def key_for_url(url):
    """
    https://r.onliner.by/ak/apartments/436768 -> r:436768
    """
    match = RE_URL_ID.search(url).groupdict()
    return f"{match['type']}:{match['id']}"


class DummyCache:

    def load_cache(self):
        pass

    def dump_cache(self) -> None:
        pass

    def has_url(self, url: str) -> bool:
        return False

    def add_url(self, url: str) -> None:
        pass

    def add_urls(self, urls: Iterable[str]):
        for url in urls:
            self.add_url(url)



class URLCacheManager(DummyCache):

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
        return key_for_url(url) in self.url_set

    def add_url(self, url: str) -> None:
        self.url_set.add(key_for_url(url))

    def add_urls(self, urls: Iterable[str]):
        for url in urls:
            self.add_url(key_for_url(url))


class RedisURLCache(DummyCache):

    __CACHE_KEY_NAME = 'urls-cache'
    __URL_FLUSH_THRESHOLD = 20

    def __init__(self, redis_client):
        self._redis_client = redis_client
        self._url_buffer = set()

    def __flush_urls(self):
        if self._url_buffer:
            self._redis_client.sadd(
                self.__CACHE_KEY_NAME,
                *self._url_buffer
            )
            self._url_buffer.clear()

    def dump_cache(self):
        self.__flush_urls()

    def add_url(self, url):
        key = key_for_url(url)
        self._url_buffer.add(key)
        if len(self._url_buffer) > self.__URL_FLUSH_THRESHOLD:
            self.__flush_urls()

    def has_url(self, url: str) -> bool:
        key = key_for_url(url)
        return self._redis_client.sismember(self.__CACHE_KEY_NAME, key)
