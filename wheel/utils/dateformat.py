# coding=utf8
#


from datetime import datetime
from datetime import timedelta


def pretty_date(time=False):
    """
        Get a datetime object or a int() Epoch timestamp and return a
        pretty string like `an hour ago`, `Yesterday`, `3 months ago`,
        `just now`, etc
    """
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now

    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return u"刚刚"
        if second_diff < 60:
            return str(second_diff) + u"秒之前"
        if second_diff < 120:
            return u"1分钟之前"
        if second_diff < 3600:
            return str(second_diff / 60) + u" 分钟之前"
        if second_diff < 7200:
            return u"一个小时之前"
        if second_diff < 86400:
            return str(second_diff / 3600) + u"小时之前"

    if day_diff == 1:
        return u"昨天"
    if day_diff < 7:
        return str(day_diff) + u" 天之前"
    if day_diff < 31:
        return str(day_diff / 7) + u" 周之前"
    if day_diff < 365:
        return str(day_diff / 30) + u" 月之前"

    return str(day_diff / 365) + u" 年之前"


if __name__ == '__main__':
    print(pretty_date(datetime.now() - timedelta(hours=18)))
    print(pretty_date(datetime.now() - timedelta(seconds=18)))
    print(pretty_date(datetime.now() - timedelta(days=18)))
    print(pretty_date(datetime.now() - timedelta(days=5)))
    print(pretty_date(datetime.now() - timedelta(days=50)))
    print(pretty_date(datetime.now() - timedelta(days=370)))