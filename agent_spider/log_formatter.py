"""
I was unable to find a proper way to suppress scrapy.core.spider
logging from spitting out all of the items parsed to the log,
so I had to override the original log formatter and
suppress it on that layer.
"""
import logging

from twisted.python.failure import Failure
from scrapy.logformatter import LogFormatter


SCRAPEDMSG = u"Scraped from %(src)s"


class SilentLogFormatter(LogFormatter):
    def scraped(self, item, response, spider):
        """Logs a message when an item is scraped by a spider."""
        if isinstance(response, Failure):
            src = response.getErrorMessage()
        else:
            src = response
        return {
            'level': logging.DEBUG,
            'msg': SCRAPEDMSG,
            'args': {
                'src': src,
            }
        }
