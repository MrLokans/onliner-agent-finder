from typing import List

from agent_spider.config import LAT_INDEX, LONG_INDEX
from agent_spider.utils import are_floats_equal


class Point(object):

    def __init__(self, latitude, longitude):
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def __repr__(self):
        return 'Point({}, {})'.format(self.latitude, self.longitude)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        latitude_equal = are_floats_equal(self.latitude, other.latitude)
        longitude_equal = are_floats_equal(self.longitude, other.longitude)
        return latitude_equal and longitude_equal


class CoordinateRectangle(object):
    """
    Represents coordinates rectangle
    used in URLS to filter apartment
    location
    """

    def __init__(self, left_bottom: Point, right_top: Point):
        self.left_bottom = left_bottom
        self.right_top = right_top

    def get_rectangles(self,
                       cols: int=2,
                       rows: int=2) -> List['CoordinateRectangle']:
        """
        Split the given rectangle into cols*rows rectangles with the same square
        """
        rectangles = []

        longitude_step = (self.right_top.longitude - self.left_bottom.longitude) / rows
        latitude_step = (self.right_top.latitude - self.left_bottom.latitude) / cols

        for row in range(rows):
            for col in range(cols):
                lb = Point(self.left_bottom.latitude + col * latitude_step,
                           self.left_bottom.longitude + row * longitude_step)
                rt = Point(self.left_bottom.latitude + (col + 1) * latitude_step,
                           self.left_bottom.longitude + (row + 1) * longitude_step)
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

    def __eq__(self, other):
        """
        Two rectangles are considered equal if
        their left bottom and right top coordinates
        are equal
        """
        if not isinstance(other, CoordinateRectangle):
            return False
        return self.left_bottom == other.left_bottom \
            and self.right_top == other.right_top
