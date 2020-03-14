# -*- coding: utf-8 -*-
__author__ = 'akm'
"""
Unit prefix library for units for powers of 10. Handles multiplication and division and
returns super scripts for attaching to displays.
"""
import math


class MetaPrefix(type):
    power_index = {}
    prefix_index = {}

    def __call__(cls, *args, **kwargs):
        obj = super(MetaPrefix, cls).__call__(*args, **kwargs)
        MetaPrefix.power_index[obj.power] = obj
        MetaPrefix.prefix_index[obj.prefix] = obj
        return obj


def has_prefix(prefix):
    """
    Is the prefix in the cache?
    :param prefix: Prefix
    :return: presence of prefix
    """
    return prefix in MetaPrefix.prefix_index


def has_power(power):
    """
    Is this power in the cache?
    :param power: Power
    :return: presence of power
    """
    return power in MetaPrefix.power_index


def get_power(power):
    """
    Get the cached power index
    :param power:
    :return: Cached Power
    """
    return MetaPrefix.power_index[power]


def get_prefix(prefix):
    """
    Get the cached prefix object
    :param prefix: prefix
    :return: Cached prefix
    """
    return MetaPrefix.prefix_index[prefix]


class Prefix(metaclass=MetaPrefix):
    """
    A SI power of 10 prefix.

    :param prefix: the abbreviated version
    :param name: the long form
    :param power: the power of 10 this refers to
    """
    supers = '\u2070', '\u00B9', '\u00B2', '\u00B3', '\u2074', '\u2075', '\u2076', '\u2077', '\u2078', '\u2079'

    __slots__ = ("prefix", "name", "power", "fmt")

    def __init__(self, prefix, name, power):
        self.prefix = prefix
        self.name = name
        self.power = power
        self.fmt = self.generate_format(power)

    def generate_format(self, power):
        """
        Generate the format

        :param power: Power raised to
        :return: Formatted unicode string
        """
        # Prepare a pretty string
        pPrefix = ''
        if power < 0:
            pPrefix = u"\u207B"
            power = -power
        if power == 0:
            return ''
        elif power < 10:
            return u"10{0}{1}".format(pPrefix, self.supers[power])
        elif power < 100:
            t = power // 10
            u = power % 10
            return u"10{0}{1}{2}".format(pPrefix, self.supers[t], self.supers[u])
        else:
            return u"10^{0}{1}".format(pPrefix, power)

    def __repr__(self):
        """
        Returns a long representation of this item
        """
        return self.fmt.encode('utf-8')

    def __str__(self):
        """
        Ascii version
        """
        return "{0.prefix}".format(self).encode('utf-8')

    def __rmul__(self, o):
        """
        Return a scalar multiplied by us.
        e.g. 5 * kilo returns 5000
        """
        return o * (10 ** self.power)

    def __mul__(self, o):
        """
        Return a scalar multiplied by us.
        e.g. 5 * kilo returns 5000
        """
        return o * (10 ** self.power)

    def __rdiv__(self, o):
        """
        Return a scalar divided by us.
        e.g. 5000 / kilo returns 5
        """
        return float(o) / (10 ** self.power)


def closest_prefix(i):
    """
    Reduce a number to a multiplier and a prefix.

    e.g `closest_prefix(1000)` returns (1.0, kilo)
    `closest_prefix(1024)` returns (1.024, kilo)

    :param i: the number to index
    :returns: a (coefficient, :mod:`Prefix`) tuple.
    """
    if i == 0:
        return 0, get_power(0)

    coefficient = abs(float(i))

    mult = 1
    if i < 0:
        mult = -1

    exponent = int(math.floor(math.log(coefficient, 10) + 0.5))
    coefficient /= 10 ** exponent

    indices = sorted(MetaPrefix.power_index.keys())

    for j, i in enumerate(indices):
        if i >= exponent:
            if i > exponent:
                i = indices[j - 1]
                delta = exponent - i
                coefficient *= 10 ** delta
            break
    exponent = get_power(i)
    return coefficient * mult, exponent
