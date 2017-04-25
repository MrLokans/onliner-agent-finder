import logging
from typing import Generator

import requests

from apartments import Apartment
from config import (
    SEARCH_BASE_URL,
    MINSK_BOUND_COORDINTATES,
    URL_FILE
)
from coordinates import CoordinateRectangle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_available_apartments(coordinate_rectangle: CoordinateRectangle) -> Generator[Apartment, None, None]:
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


def get_apartment_urls() -> Generator[str, None, None]:
    url_cache = set()
    coordinate_rectangle = CoordinateRectangle.from_dict(MINSK_BOUND_COORDINTATES)
    for coord in coordinate_rectangle.get_rectangles(6, 6):
        for ap in get_available_apartments(coord):
            if ap.url in url_cache:
                continue
            url_cache.add(ap.url)
            yield ap.url


def main():
    with open(URL_FILE, 'w+') as f:
        for url in get_apartment_urls():
            f.write('{}\n'.format(url))


if __name__ == '__main__':
    main()
