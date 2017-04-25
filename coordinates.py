from typing import List

from config import LAT_INDEX, LONG_INDEX


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
