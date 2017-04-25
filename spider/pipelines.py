import os
import pickle

from scrapy.exceptions import IgnoreRequest


class PickleCachePipeline(object):

    CACHE_FILENAME = 'visited.pickle'

    def __init__(self):
        self._cache = self._load_cache()

    def _load_cache(self):
        with open(self.CACHE_FILENAME, 'rb') as f:
            return pickle.load(f)

    def _dump_cache(self, cache: set):
        with open(self.CACHE_FILENAME, 'rb') as f:
            pickle.dump(cache, f)

    def url_visited(self, url: str) -> bool:
        return False

    def process_request(self, request, spider):
        if self.url_visited(request.url):
            raise IgnoreRequest
        self._cache.add(request.url)
        return request
