# -*- coding: utf-8 -*-
from __future__ import annotations

from quantity.unit import Unit, get_unit, has_unit, NoUnit
from quantity.prefix import closest_prefix, has_prefix, get_prefix, Prefix
import quantity.prefix.prefixes as prefixes


class Quantity:
    """
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

    >>> frame = Unit('f', "frame")
    >>> frames = Quantity(432000, "frame")
    >>> runningTime = Quantity(120 * 60, 's')
    >>> fps = frames / runningTime
    >>> fps
    60.0 f/s

    :param amount: The scalar amount
    :param unit: The unit, this can be a string (with optional power prefix) or a :mod:`Unit` object.
    :param prefix: A SI power prefix to be applied to the amount.
    """

    def __init__(self, amount, unit: Unit | str = NoUnit, prefix: Prefix = prefixes.NoPrefix):
        self.amount = amount
        self.unit = unit
        self.prefix = prefix
        self._reduce_self()

    def __int__(self) -> int:
        return int((self.amount * self.prefix) + 0.5)

    def __float__(self) -> float:
        return float(self.amount * self.prefix)

    def __add__(self, o: int | float | Quantity) -> Quantity:
        if isinstance(o, (int, float)) and o == 0:
            return self

        if self.unit is NoUnit and isinstance(o, (int, float)):
            return Quantity(type(o)(self) + o)

        unit = self.unit + o.unit
        return Quantity(float(self) + float(o), unit)

    __radd__ = __add__

    def __sub__(self, o: int | float | Quantity) -> Quantity:
        if self.unit is NoUnit and isinstance(o, (int, float)):
            return Quantity(type(o)(self) - o)

        unit = self.unit - o.unit
        return Quantity(float(self) - float(o), unit)

    def __mul__(self, o) -> Quantity:
        if isinstance(o, Quantity):
            unit = self.unit * o.unit
            return Quantity(float(self) * float(o), unit)

        unit = self.unit
        return Quantity(type(o)(self) * o, unit)

    __rmul__ = __mul__

    def __truediv__(self, o: int | float | Quantity) -> Quantity:
        if isinstance(o, Quantity):
            unit = self.unit / o.unit
            return Quantity(float(self) / float(o), unit)

        unit = self.unit
        return Quantity(type(o)(self) / o, unit)

    def _reduce_self(self):
        """
        Parse our unit and reduce ourselves to the smallest representation
        """
        if isinstance(self.unit, str):
            self.unit = self.__find_unit()
        a = self.amount * self.prefix
        self.amount, self.prefix = closest_prefix(a)

    def _strip_unit(self):
        """
        Remove our unit type
        """
        self.unit = NoUnit

    def __find_unit(self) -> Unit:
        """
        Take a string like kV and work out prefix and units, obviously
        there is scope for collision between units and prefixes...

        :return: :mod:`Unit` object
        """
        if not self.unit:
            return NoUnit

        if isinstance(self.unit, Unit):
            return self.unit

        u = self.unit
        if has_unit(u):
            return get_unit(u)

        # Work backwards through the list trying to find a unit that matches
        unit = self.unit = None
        ul = list(u)
        u = ""

        while ul:
            u = (ul.pop() + u)
            if has_unit(u):
                unit = get_unit(u)
                break

        # Nothing left to look at
        if not ul:
            if not unit:
                # Make a temporary unit, since we don't know what this is
                unit = Unit(u, u, temp=True)
            return unit

        # We have leftovers... this should be a prefix...
        ul = ''.join(ul)
        if has_prefix(ul):
            self.amount *= get_prefix(ul)
        return unit

    def __repr__(self) -> str:
        return f'{self.amount} {self.prefix}{self.unit}'

    def __str__(self) -> str:
        return f'{self.amount} {self.prefix}{self.unit}'

    def __eq__(self, other: int | float | Quantity) -> bool:
        """
        Equivalence checking.
        If we have no unit, then we will compare against scalars.

        Otherwise, everything else has to match
        """
        if self.unit is NoUnit and isinstance(other, (int, float)):
            return type(other)(self) == other

        return (other.amount == self.amount and
                other.unit is self.unit and
                other.prefix is self.prefix)

    def __ne__(self, other: int | float | Quantity) -> bool:
        return not (other == self)

    def __lt__(self, other: int | float | Quantity) -> bool:
        if self.unit is NoUnit and isinstance(other, (int, float, int)):
            return type(other)(self) > other

        assert other.unit is self.unit and other.prefix is self.prefix
        return self.amount < other.amount

    def __le__(self, other: int | float | Quantity) -> bool:
        if self.unit is NoUnit and isinstance(other, (int, float, int)):
            return type(other)(self) <= other

        assert other.unit is self.unit and other.prefix is self.prefix
        return self.amount <= other.amount

    def __gt__(self, other: int | float | Quantity) -> bool:
        if self.unit is NoUnit and isinstance(other, (int, float, int)):
            return type(other)(self) > other

        assert other.unit is self.unit and other.prefix is self.prefix
        return self.amount > other.amount

    def __ge__(self, other: int | float | Quantity) -> bool:
        if self.unit is NoUnit and isinstance(other, (int, float, int)):
            return type(other)(self) >= other

        assert other.unit is self.unit and other.prefix is self.prefix
        return self.amount >= other.amount

    def convert(self, unit: Unit) -> Quantity:
        return Quantity(self.unit.convert(unit, float(self)), unit)

    def to(self, prefix: Prefix | str) -> float | None:
        """
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

        if has_prefix(prefix):
            return int(self) / get_prefix(prefix)

        return None
