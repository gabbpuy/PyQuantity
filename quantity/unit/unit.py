# -*- coding: utf-8 -*-
"""
A class representing a unit of measure. Similar units can be added or subtracted, while any two units can be multiplied
or divided. There are some lookups for units that can be derived from multiplying or dividing two units.
"""


class MetaUnit(type):
    unitIndex = {}
    combinedUnits = {}
    dividedUnits = {}
    conversions = {}

    def __call__(cls, *args, **kwargs):
        """
        Add units when a Unit is created
        """
        obj = super(MetaUnit, cls).__call__(*args, **kwargs)
        if not ('temp' in kwargs and kwargs.get('temp')) or (len(args) == 3 and not args[-1]):
            MetaUnit.unitIndex[obj.unit] = obj
            MetaUnit.unitIndex[obj.name] = obj
        return obj


class Unit(metaclass=MetaUnit):
    """
    An SI unit of measure.

    :param unit: The unit abbreviation
    :param name: The name of the unit
    :param temp: Is this a temporary unit (created when combining units)
    """

    xNames = ('', '', 'square ', 'cubic ', 'quartic')

    # Unicode superscripts for powers , 0, 1, 2, 3, 4, 5 etc..
    supers = '\u2070', '\u00B9', '\u00B2', '\u00B3', '\u2074', '\u2075', '\u0076', '\u0077', '\u0078', '\u2079'

    __slots__ = ('unit', 'name', '_unit', 'index', 'xName')

    # temp is parsed by the meta class...
    def __init__(self, unit, name, temp=False):
        self.unit = unit
        self._unit = unit
        self.name = name
        self.index = 1
        self.xName = ''

    def __add__(self, o):
        assert o is self
        return self

    def __sub__(self, o):
        assert o is self
        return self

    # XXX mul and div need a new MultiUnit class that takes care of this
    # and can deal with m/s/s actually being m/s² or ms-²

    def __mul__(self, o):
        """
        Multiple two units
        """
        if self is NoUnit:
            unit = o
        elif o is NoUnit:
            unit = self
        elif self._unit != o._unit:
            k = frozenset((o, self))
            if has_combined_unit(k):
                unit = get_combined_unit(k)
            else:
                # Build a temporary unit
                unit = Unit(u"{0}{1}".format(self.unit, o.unit),
                            u"{0}-{1}".format(self.name, o.name),
                            temp=True)
        else:
            unit = Unit(self._unit, self.name, True)
            index = self.index + o.index - 1
            for i in range(index):
                unit._up()
        return unit

    def __truediv__(self, o):
        """
        Divide two units
        """
        unit = self
        if o is NoUnit:
            pass
        elif unit is not o:
            k = (self, o)
            if self._unit == o._unit:
                unit = Unit(self._unit, self.name, temp=True)
                unit.index = self.index + o.index
                for i in range(self.index - o.index + 1):
                    unit._down()
                if unit.index == 1:
                    unit = unit._unit
            elif has_divided_unit(k):
                unit = get_divided_unit(k)
            else:
                unit = Unit(u"{0}/{1}".format(self.unit, o.unit),
                            u"{0} per {1}".format(self.name, o.name),
                            temp=True)
        else:
            unit = NoUnit

        return unit

    def _up(self):
        """
        Increase our exponent
        """
        self.index += 1
        self._updateName()
        self._updateUnit()

    def _down(self):
        """
        decrease our exponent
        """
        self.index -= 1
        self._updateName()
        self._updateUnit()

    def _updateUnit(self):
        """
        Our unit changed to have an exponent, update our representation
        """
        if self.index > 1:
            if self.index < 10:
                self.unit = '{0}{1}'.format(self._unit, self.supers[self.index])
            elif self.index < 100:
                t, u = divmod(self.index, 10)
                self.unit = '{0}{1}{2}'.format(self._unit, self.supers[t], self.supers[u])
            else:
                self.unit = '{0}^{1}'.format(self._unit, self.index)
        else:
            self.unit = self._unit

    def _updateName(self):
        """
        Our unit changed to have an exponent, update our representation
        """
        if 1 <= self.index <= 4:
            self.xName = self.xNames[self.index]
        else:
            self.xName = '{0}th '.format(self.index)

    def __repr__(self):
        return '{0}{1}'.format(self.xName, self.name).encode('utf-8')

    def __str__(self):
        return self.unit.encode('utf-8')

    def convert(self, to, value):
        """
        Convert from this to another unit

        :param to: desired :mod:`Unit`
        :param value: starting value
        :return: unitless value
        """
        operations = get_conversion((self, to))
        for operation, v in operations:
            value = operation(value, v)
        return value

    @staticmethod
    def NoUnit():
        return Unit("", "")


# Empty Unit
NoUnit = Unit.NoUnit()


def get_units() -> tuple:
    """
    Get all the units
    :return:
    """
    return tuple(MetaUnit.unitIndex.keys())


def get_all_conversions() -> dict:
    return MetaUnit.conversions


def get_all_divided_units() -> dict:
    return MetaUnit.dividedUnits


def get_all_combined_units() -> dict:
    return MetaUnit.combinedUnits


def get_unit(unitName) -> Unit:
    return MetaUnit.unitIndex[unitName]


def get_combined_unit(unit) -> Unit:
    return MetaUnit.combinedUnits[unit]


def get_conversion(units):
    return MetaUnit.conversions.get(units)


def get_divided_unit(unit) -> Unit:
    return MetaUnit.dividedUnits[unit]


def has_unit(unit_id: str) -> bool:
    return unit_id in MetaUnit.unitIndex


def has_combined_unit(unit_id) -> bool:
    return unit_id in MetaUnit.combinedUnits


def has_conversion(units) -> bool:
    return units in MetaUnit.conversions


def has_divided_unit(units) -> bool:
    return units in MetaUnit.dividedUnits
