# -*- coding: utf-8 -*-
from __future__ import annotations
import math
"""
Unit prefix library for units for powers of 10. Handles multiplication and division and
returns super scripts for attaching to displays.
"""



class MetaPrefix(type):
    power_index = {}
    prefix_index = {}

    def __call__(cls, *args, **kwargs):
        obj = super(MetaPrefix, cls).__call__(*args, **kwargs)
        MetaPrefix.power_index[obj.power] = obj
        MetaPrefix.prefix_index[obj.prefix] = obj
        return obj


class Prefix(metaclass=MetaPrefix):
    """
    A SI power of 10 prefix.

    :param prefix: the abbreviated version
    :param name: the long form
    :param power: the power of 10 this refers to
    """
    supers = ('⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹')

    __slots__ = ("prefix", "name", "power", "fmt")

    def __init__(self, prefix: str, name: str, power: int):
        self.prefix = prefix
        self.name = name
        self.power = power
        self.fmt = self.generate_format(power)

    def generate_format(self, power: int) -> str:
        """
        Generate the format

        :param power: Power raised to
        :return: Formatted unicode string
        """
        # Prepare a pretty string
        pPrefix = ''
        if power < 0:
            pPrefix = "⁻"
            power = -power
        if power == 0:
            return ''
        elif power < 10:
            return f'10{pPrefix}{self.supers[power]}'
        elif power < 100:
            t, u = divmod(power, 10)
            return f'10{pPrefix}{self.supers[t]}{self.supers[u]}'

        return f'10^{pPrefix}{power}'

    def __repr__(self) -> str:
        """
        Returns a long representation of this item
        """
        return self.fmt

    def __str__(self) -> str:
        return f'{self.prefix}'

    def __rmul__(self, o) -> int | float:
        """
        Return a scalar multiplied by us.
        e.g. 5 * kilo returns 5000
        """
        return o * (10 ** self.power)

    def __mul__(self, o) -> int | float:
        """
        Return a scalar multiplied by us.
        e.g. 5 * kilo returns 5000
        """
        return o * (10 ** self.power)

    def __rtruediv__(self, o) -> int | float:
        """
        Return a scalar divided by us.
        e.g. 5000 / kilo returns 5
        """
        return float(o) / (10 ** self.power)


def closest_prefix(i: int | float) -> tuple:
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


def has_prefix(prefix: str) -> bool:
    """
    Is the prefix in the cache?
    :param prefix: Prefix
    :return: presence of prefix
    """
    return prefix in MetaPrefix.prefix_index


def has_power(power: int) -> bool:
    """
    Is this power in the cache?
    :param power: Power
    :return: presence of power
    """
    return power in MetaPrefix.power_index


def get_power(power: int) -> int:
    """
    Get the cached power index
    :param power:
    :return: Cached Power
    """
    return MetaPrefix.power_index[power]


def get_prefix(prefix: str) -> Prefix:
    """
    Get the cached prefix object
    :param prefix: prefix
    :return: Cached prefix
    """
    return MetaPrefix.prefix_index[prefix]

