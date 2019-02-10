import argparse
import logging
from typing import Iterable

import requests
from tqdm import tqdm

from agent_spider.config import (
    RENTED_APARTMENTS_SEARCH_API_URL,
    MINSK_BOUND_COORDINTATES,
    DEFAULT_URL_FILE,
    SOLD_APARTMENTS_SEARCH_API_URL)
from agent_spider.coordinates import CoordinateRectangle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging\
    .getLogger('requests.packages.urllib3.connectionpool')\
    .setLevel(logging.INFO)

DEFAULT_RECTANGLES_SIZE = (6, 6)


def get_apartment_urls_for_rectangle(coordinate_rectangle: CoordinateRectangle) -> Iterable[str]:
    urls_to_check = (SOLD_APARTMENTS_SEARCH_API_URL, RENTED_APARTMENTS_SEARCH_API_URL)
    for url_to_check in urls_to_check:
        session = requests.Session()
        payload = coordinate_rectangle.to_url_params()

        req = session.get(url_to_check, params=payload)
        req = req.json()

        total_pages = req['page']['last']

        for i in range(1, total_pages + 1):
            payload.update({'page': i})
            resp = session.get(url_to_check, params=payload)
            for ap in resp.json()['apartments']:
                yield ap['url']


def get_apartment_urls() -> Iterable[str]:
    """
    Gets all available apartment links,
    by splitting the map into several chunks
    and requesting the data to avoid API limits
    """
    url_cache = set()
    coordinate_rectangle = CoordinateRectangle.from_dict(MINSK_BOUND_COORDINTATES)
    rectangles = coordinate_rectangle.get_rectangles(*DEFAULT_RECTANGLES_SIZE)
    for coord in tqdm(rectangles):
        for url in get_apartment_urls_for_rectangle(coord):
            if url in url_cache:
                continue
            url_cache.add(url)
            yield url


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-file',
                        help='File to write collected URLS to.',
                        default=DEFAULT_URL_FILE)
    args = parser.parse_args()

    with open(args.output_file, 'w') as f:
        for url in get_apartment_urls():
            f.write('{}\n'.format(url))


if __name__ == '__main__':
    main()
