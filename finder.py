import datetime
import logging
from typing import Generator, List

import requests

from config import (
	RENT_TYPE,
    SEARCH_BASE_URL,
	URL_FILE,
    MINSK_BOUND_COORDINTATES,
    LAT_INDEX, LONG_INDEX
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ApartmentIsNotFound(Exception):
    pass


class Point(object):

    def __init__(self, latitude, longitude):
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def __repr__(self):
        return 'Point({}, {})'.format(self.latitude, self.longitude)

    def __str__(self):
        return self.__repr__()


class CoordinateRectangle(object):

    def __init__(self, left_bottom: Point, right_top: Point):
        self.left_bottom = left_bottom
        self.right_top = right_top

    def get_rectangles(self, n: int=2, k: int=2) -> List['CoordinateRectangle']:
        """
        Split the given rectangle into n*k rectangles with the same square

        """
        rectangles = []

        longitude_step = abs(self.left_bottom.longitude - self.right_top.longitude) / n
        latitude_step = abs(self.left_bottom.latitude - self.right_top.latitude) / k

        for y in range(n):
            for x in range(k):
                lb = Point(self.left_bottom.latitude + x * latitude_step,
                           self.right_top.longitude + y * longitude_step)
                rt = Point(self.left_bottom.latitude + (x + 1) * latitude_step,
                           self.right_top.longitude + (y + 1) * longitude_step)
                rectangles.append(CoordinateRectangle(lb, rt))
        return rectangles

    def __repr__(self):
        return 'CoordinateRectangle({0}, {1})'.format(self.left_bottom, self.right_top)

    def __str__(self):
        return self.__repr__()

    @classmethod
    def from_dict(cls, d):
        lb = Point(d['lb'][LAT_INDEX], d['lb'][LONG_INDEX])
        rt = Point(d['rt'][LAT_INDEX], d['rt'][LONG_INDEX])
        return cls(lb, rt)

    def to_url_params(self):
        return {
            'bounds[lb][lat]': self.left_bottom.latitude,
            'bounds[lb][long]': self.left_bottom.longitude,
            'bounds[rt][lat]': self.right_top.latitude,
            'bounds[rt][long]': self.right_top.longitude,
        }


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


def build_url_bounds_params(bound: dict) -> dict:
    params['[lb][lat]'] = MINSK_BOUND_COORDINTATES['lb'][LAT_INDEX]
    params['[lb][long]'] = MINSK_BOUND_COORDINTATES['lb'][LONG_INDEX]
    params['[rt][lat]'] = MINSK_BOUND_COORDINTATES['rt'][LAT_INDEX]
    params['[rt][long]'] = MINSK_BOUND_COORDINTATES['rt'][LONG_INDEX]


def get_available_apartments(coordinate_rectangle: CoordinateRectangle) -> Generator[Apartment, None, None]:
    session = requests.Session()
    payload = coordinate_rectangle.to_url_params()
    squares = get_squares_from_minsk_coordinates()

    payloads = [build_url_bounds_params(square) for square in squares]
    [payload.update({'only_owner': 'true'}) for payload in payloads]

    for payload in payloads:
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


def main():
    url_cache = set()
    with open('apartment_urls.txt', 'w+') as f:
        coordinate_rectangle = CoordinateRectangle\
            .from_dict(MINSK_BOUND_COORDINTATES)
        for coord in coordinate_rectangle.get_rectangles():
            for ap in get_available_apartments(coord):
                if ap.url in url_cache:
                    continue
                f.write(ap.url)
                f.write('\n')
                url_cache.add(ap.url)


if __name__ == '__main__':
    main()
