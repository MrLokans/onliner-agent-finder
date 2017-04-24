import datetime
import logging
from typing import Generator

import requests

from config import (
    SEARCH_BASE_URL,
    MINSK_BOUND_COORDINTATES,
    LAT_INDEX, LONG_INDEX
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ApartmentIsNotFound(Exception):
    pass


class Apartment(object):
    __slots__ = ('id', 'created_at', 'last_time_up',
                 'contact',
                 'location', 'photo', 'price', 'rent_type',
                 'up_available_in', 'url', 'origin_url')

    DEFAULT_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S+0300'

    def __init__(self, id,
                 created_at: datetime.datetime,
                 last_time_up: datetime.datetime,
                 location: dict,
                 contact: dict,
                 photo: str, price: dict, rent_type: str,
                 up_available_in: int, url: str,
                 origin_url: str):
        self.id = id
        self.contact = contact
        self.created_at = created_at
        self.last_time_up = last_time_up
        self.location = location
        self.photo = photo
        self.price = price
        self.rent_type = rent_type
        self.up_available_in = up_available_in
        self.url = url
        self.origin_url = origin_url

    @classmethod
    def from_dict(cls, d):
        if isinstance(d['created_at'], str):
            d['created_at'] = cls.__datetime_from_str(d['created_at'])
        if isinstance(d['last_time_up'], str):
            d['last_time_up'] = cls.__datetime_from_str(d['last_time_up'])
        return cls(**d)

    def to_dict(self):
        d = {}
        for k in self.__slots__:
            d[k] = getattr(self, k, None)
        return d

    @classmethod
    def __datetime_from_str(cls, s: str) -> datetime.datetime:
        return datetime.datetime.strptime(s, cls.DEFAULT_DATE_FORMAT)

    def __repr__(self):
        return 'Apartment(id={}, url={})'.format(self.id, self.url)

    def __str__(self):
        return self.__repr__()


def build_url_bounds_params(bound: dict = MINSK_BOUND_COORDINTATES) -> dict:
    params = {}
    params['[lb][lat]'] = bound['lb'][LAT_INDEX]
    params['[lb][long]'] = bound['lb'][LONG_INDEX]
    params['[rt][lat]'] = bound['rt'][LAT_INDEX]
    params['[rt][long]'] = bound['rt'][LONG_INDEX]
    return params


def get_average_from_two_points(p1, p2):
    return (
        (float(p1[LAT_INDEX]) + float(p2[LAT_INDEX])) / 2.0,
        (float(p1[LONG_INDEX]) + float(p2[LONG_INDEX])) / 2.0
    )


def get_squares_from_minsk_coordinates():
    left_bottom_point = MINSK_BOUND_COORDINTATES['lb']
    right_top_point = MINSK_BOUND_COORDINTATES['rt']
    right_bottom_point = (right_top_point[LAT_INDEX], left_bottom_point[LONG_INDEX])
    left_top_point = (left_bottom_point[LAT_INDEX], right_top_point[LONG_INDEX])

    center_point = get_average_from_two_points(right_top_point, left_bottom_point)

    right_top_square = {
        'rt': right_top_point,
        'lb': center_point
    }

    left_top_square = {
        'rt': get_average_from_two_points(left_top_point, right_top_point),
        'lb': get_average_from_two_points(left_top_point, left_bottom_point)
    }

    right_bottom_square = {
        'rt': get_average_from_two_points(right_top_point, right_bottom_point),
        'lb': get_average_from_two_points(left_bottom_point, right_bottom_point)
    }

    left_bottom_square = {
        'rt': center_point,
        'lb': left_bottom_point
    }

    return left_top_square, right_top_square, left_bottom_square, right_bottom_square


def get_available_apartments() -> Generator[Apartment, None, None]:
    session = requests.Session()

    squares = get_squares_from_minsk_coordinates()

    payloads = [build_url_bounds_params(square) for square in squares]
    [payload.update({'only_owner': 'true'}) for payload in payloads]

    for payload in payloads:
        req = session.get(SEARCH_BASE_URL, params=payload)
        req = req.json()

        total_pages = req['page']['last']

        for i in range(2, total_pages + 1):
            payload.update({'page': i})
            resp = session.get(SEARCH_BASE_URL, params=payload)
            for ap in resp.json()['apartments']:
                data = ap.copy()
                data.update({'origin_url': resp.url})
                yield Apartment.from_dict(data)


def main():
    url_cache = set()
    with open('apartment_urls.txt', 'w+') as f:
        for ap in get_available_apartments():
            if ap.url in url_cache:
                continue
            f.write(ap.url)
            f.write('\n')
            url_cache.add(ap.url)


if __name__ == '__main__':
    main()
