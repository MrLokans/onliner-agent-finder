import argparse
import logging
from typing import Iterable

import requests
from tqdm import tqdm

from agent_spider.apartments import Apartment
from agent_spider.config import (
    SEARCH_BASE_URL,
    MINSK_BOUND_COORDINTATES,
    DEFAULT_URL_FILE
)
from agent_spider.coordinates import CoordinateRectangle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging\
    .getLogger('requests.packages.urllib3.connectionpool')\
    .setLevel(logging.INFO)

DEFAULT_RECTANGLES_SIZE = (6, 6)


def get_available_apartments(coordinate_rectangle: CoordinateRectangle) -> Iterable[Apartment]:
    session = requests.Session()
    payload = coordinate_rectangle.to_url_params()

    req = session.get(SEARCH_BASE_URL, params=payload)
    req = req.json()

    total_pages = req['page']['last']

    for i in range(1, total_pages + 1):
        payload.update({'page': i})
        resp = session.get(SEARCH_BASE_URL, params=payload)
        for ap in resp.json()['apartments']:
            data = ap.copy()
            data.update({'origin_url': resp.url})
            yield Apartment.from_dict(data)


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
        for ap in get_available_apartments(coord):
            if ap.url in url_cache:
                continue
            url_cache.add(ap.url)
            yield ap.url


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
