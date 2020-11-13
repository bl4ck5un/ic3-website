import datetime

import yaml
from dateutil import parser


class Press(object):
    def __init__(self, title, url, venue, date):
        self.title = title
        self.url = url
        self.venue = venue
        self.date = date
        self.date_str = date.strftime("%B %d, %Y")

        self.type = 'news'

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        s = '- Press: [%s](%s) by **%s** on %s' % (self.title, self.url, self.venue, self.date_str)
        return s.encode('utf-8')


def _read_events_from_yaml(filename, get_featured=False):
    with open(filename, 'r') as yaml_file:
        events = yaml.full_load(yaml_file)
        if get_featured:
            press_items = [Press(e['title'], e['url'], e['venue'], parser.parse(e['date']).date())
                           for e in events if e['tags'].contains('featured')]
        else:
            press_items = [Press(e['title'], e['url'], e['venue'], parser.parse(e['date']).date()) for e in events]

    return sorted(press_items, key=lambda x: x.date, reverse=True)


def get_all_press(expire_in_days=None):
    if expire_in_days and expire_in_days < -1:
        raise Exception('expire_in_days must > 0')

    press = _read_events_from_yaml('content/press/pressroll.yaml')

    # None == don't filter at all
    if expire_in_days is None:
        return press

    today = datetime.date.today()

    def not_expired(item):
        delta = today - item.date
        return delta.days <= expire_in_days

    press = list(filter(not_expired, press))
    return sorted(press, key=lambda x: x.date, reverse=True)


def get_featured_press(expire_in_days):
    """
    :return: a list of press items with a 'featured' tag
    """
    press_featured = _read_events_from_yaml('content/press/pressroll.yaml')

    today = datetime.date.today()

    def not_expired(item):
        delta = today - item.date
        return delta.days <= expire_in_days

    press_featured = list(filter(not_expired, press_featured))
    return sorted(press_featured, key=lambda x: x.date, reverse=True)
