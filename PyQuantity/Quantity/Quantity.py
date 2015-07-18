# -*- coding: utf-8 -*-
__author__ = "akm"

import PyQuantity.Unit as Unit
import PyQuantity.Prefix as Prefix

Units = Unit.Units
NO_UNIT = Units.NoUnit


class Quantity(object):
    u"""
    A Quantity class. A Quantity is a scalar amount with a unit. This class
    also reduces to SI prefixes like kilo and mega for display, but, can be
    used as a scalar.

    >>> q = Quantity(1.0, "MV")
    >>> q
    1.0 MV
    >>> q = Quantity(1000000, 'V')
    >>> q
    1.0 MV
    >>> q.to('V')
    1000000.0
    >>> volts = Quantity(10, 'V')
    >>> amps = Quantity(100, 'A')
    >>> volts * amps
    1.0 kW
    >>> volts / amps
    100.0 mΩ

    You can define your own units. We can get frames per second by defining frames.

    >>> frame = Unit.Unit('f', "frame")
    >>> frames = Quantity(432000, "frame")
    >>> runningTime = Quantity(120 * 60, 's')
    >>> fps = frames / runningTime
    >>> fps
    60.0 f/s

    :param amount: The scalar amount
    :param unit: The unit, this can be a string (with optional power prefix) or a :mod:`Unit` object.
    :param prefix: A SI power prefix to be applied to the amount.
    """

    def __init__(self, amount, unit = NO_UNIT, prefix = Prefix.Prefixes.NoPrefix):
        self.amount = amount
        self.unit = unit
        self.prefix = prefix
        self._reduceSelf()

    def __int__(self):
        return int((self.amount * self.prefix) + 0.5)

    def __long__(self):
        return long((self.amount * self.prefix) + 0.5)

    def __float__(self):
        return float(self.amount * self.prefix)

    def __add__(self, o):
        if isinstance(o, (int, long, float)) and o == 0:
            return self

        if self.unit is NO_UNIT and isinstance(o, (int, long, float)):
            return Quantity(type(o)(self) + o)

        unit = self.unit + o.unit
        return Quantity(float(self) + float(o), unit)

    __radd__ = __add__

    def __sub__(self, o):
        if self.unit is NO_UNIT and isinstance(o, (int, long, float)):
            return Quantity(type(o)(self) - o)

        unit = self.unit - o.unit
        return Quantity(float(self) - float(o), unit)

    def __mul__(self, o):
        if isinstance(o, Quantity):
            unit = self.unit * o.unit
            return Quantity(float(self) * float(o), unit)

        unit = self.unit
        return Quantity(type(o)(self) * o, unit)

    __rmul__ = __mul__

    def __div__(self, o):
        if isinstance(o, Quantity):
            unit = self.unit / o.unit
            return Quantity(float(self) / float(o), unit)

        unit = self.unit
        return Quantity(type(o)(self) / o, unit)

    def _reduceSelf(self):
        """
        Parse our unit and reduce ourselves to the smallest representation
        """
        if isinstance(self.unit, basestring):
            self.unit = self.__findUnit()
        a = self.amount * self.prefix
        self.amount, self.prefix = Prefix.closestPrefix(a)

    def _stripUnit(self):
        """
        Remove our unit type
        """
        self.unit = NO_UNIT

    def __findUnit(self):
        """
        Take a string like kV and work out prefix and units, obviously
        there is scope for collision between units and prefixes...

        :return: :mod:`Unit` object
        """
        if not self.unit:
            return NO_UNIT

        if isinstance(self.unit, Unit.Unit):
            return self.unit

        u = self.unit
        if Unit.hasUnit(u):
            return Unit.getUnit(u)

        # Work backwards through the list trying to find a unit that matches
        unit = self.unit = None
        ul = list(u)
        u = ""

        while ul:
            u = (ul.pop() + u)
            if Unit.hasUnit(u):
                unit = Unit.getUnit(u)
                break

        # Nothing left to look at
        if not ul:
            if not unit:
                # Make a temporary unit, since we don't know what this is
                unit = Unit.Unit(u, u, True)
            return unit

        # We have left overs... this should be a prefix...
        ul = ''.join(ul)
        if Prefix.hasPrefix(ul):
            self.amount *= Prefix.getPrefix(ul)
        return unit

    def __repr__(self):
        return u"{0.amount} {0.prefix}{0.unit}".format(self).encode('utf-8')

    def __str__(self):
        return u"{0.amount} {0.prefix}{0.unit}".format(self).encode('utf-8')

    def __unicode__(self):
        return u"{0.amount} {0.prefix}{0.unit}".format(self)

    def __eq__(self, other):
        """
        Equivalence checking.
        If we have no unit, then we will compare against scalars.

        Otherwise everything else has to match
        """
        if self.unit is NO_UNIT and isinstance(other, (int, float, long)):
            return type(other)(self) == other

        return (other.amount == self.amount and
                other.unit is self.unit and
                other.prefix is self.prefix)

    def __ne__(self, other):
        return not (other == self)

    def __lt__(self, other):
        if self.unit is NO_UNIT and isinstance(other, (int, float, long)):
            return type(other)(self) > other

        assert other.unit is self.unit and other.prefix is self.prefix
        return self.amount < other.amount

    def __le__(self, other):
        if self.unit is NO_UNIT and isinstance(other, (int, float, long)):
            return type(other)(self) <= other

        assert other.unit is self.unit and other.prefix is self.prefix
        return self.amount <= other.amount

    def __gt__(self, other):
        if self.unit is NO_UNIT and isinstance(other, (int, float, long)):
            return type(other)(self) > other

        assert other.unit is self.unit and other.prefix is self.prefix
        return self.amount > other.amount

    def __ge__(self, other):
        if self.unit is NO_UNIT and isinstance(other, (int, float, long)):
            return type(other)(self) >= other

        assert other.unit is self.unit and other.prefix is self.prefix
        return self.amount >= other.amount

    def convert(self, unit):
        return Quantity(self.unit.convert(unit, float(self)), unit)

    def to(self, prefix):
        u"""
        Convert to different prefix (i.e. seconds to ms) with no units e.g.

        >>> q = Quantity(1, 'km')
        >>> q
        1.0 km
        >>> q.to('m')
        1000.0
        >>> q.to('mm')
        1000000.0
        >>> q.to('Mm')
        0.001

        :param prefix: A prefix / unit to convert to
        :return: A floating point scalar or None for invalid prefix
        """
        if prefix.endswith(self.unit.unit):
            prefix = prefix[:-len(self.unit.unit)]

        if Prefix.hasPrefix(prefix):
            return int(self) / Prefix.getPrefix(prefix)

        return None