# -*- coding: utf-8 -*-
from datetime import datetime


def filter_by_timerange(range, qry, prop):
    """Filter by time range
    """
    if range[0] not in ('<', '('):
        raise ValueError('Invalid time range given, must start from ( or <')
    if range[-1] not in ('>', ')'):
        raise ValueError('Invalid time range given, must end with ) or >')

    # TODO validate :
    try:
        fromtime, totime = range.split(':')
    except ValueError:
        raise ValueError("Start and end date must be splitted by ':'")

    if fromtime[1:]:
        if range[0] == '(':
            qrytime = int(fromtime[1:])+1
        elif range[0] == '<':
            qrytime = int(fromtime[1:])
        else:
            raise ValueError('Inavlid time range start given: {}'.format(
                range))
        qry = qry.filter(prop > datetime.fromtimestamp(qrytime))

    if totime[:-1]:
        if range[-1] == ')':
            qrytime = int(totime[:-1])
        elif range[-1] == '>':
            qrytime = int(totime[:-1])+1
        else:
            raise ValueError('Inavlid time range end given: {}'.format(
                range))
        print qrytime
        qry = qry.filter(prop < datetime.fromtimestamp(qrytime))

    return qry
