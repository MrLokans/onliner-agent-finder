import datetime


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
