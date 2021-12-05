# -*- coding: utf-8 -*-
"""
A class representing a unit of measure. Similar units can be added or subtracted, while any two units can be multiplied
or divided. There are some lookups for units that can be derived from multiplying or dividing two units.
"""
from typing import Union


class MetaUnit(type):
    unit_index = {}
    combined_units = {}
    divided_units = {}
    conversions = {}

    def __call__(cls, *args, **kwargs):
        """
        Add units when a Unit is created
        """
        obj = super(MetaUnit, cls).__call__(*args, **kwargs)
        if not ('temp' in kwargs and kwargs.get('temp')) or (len(args) == 3 and not args[-1]):
            MetaUnit.unit_index[obj.unit] = obj
            MetaUnit.unit_index[obj.name] = obj
        return obj


class Unit(metaclass=MetaUnit):
    """
    An SI unit of measure.

    :param unit: The unit abbreviation
    :param name: The name of the unit
    :param temp: Is this a temporary unit (created when combining units)
    """

    x_names = ('', '', 'square ', 'cubic ', 'quartic', 'quintic', 'sextic', 'septic', 'octic', 'nonic', 'decic')

    # Unicode superscripts for powers , 0, 1, 2, 3, 4, 5 etc..
    supers = ('⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹')

    __slots__ = ('unit', 'name', '_unit', 'index', 'x_name')

    # temp is parsed by the meta class...
    def __init__(self, unit: str, name: str, temp: bool = False):
        self.unit = unit
        self._unit = unit
        self.name = name
        self.index = 1
        self.x_name = ''

    def __add__(self, o):
        assert o is self
        return self

    def __sub__(self, o):
        assert o is self
        return self

    # XXX mul and div need a new MultiUnit class that takes care of this
    # and can deal with m/s/s actually being m/s² or ms-²

    def __mul__(self, o: 'Unit') -> 'Unit':
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
                unit = Unit(f'{self.unit}{o.unit}',
                            f'{self.name}-{o.name}',
                            temp=True)
        else:
            unit = Unit(self._unit, self.name, True)
            index = self.index + o.index - 1
            for i in range(index):
                unit._up()
        return unit

    def __truediv__(self, o: 'Unit') -> 'Unit':
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
                unit = Unit(f'{self.unit}/{o.unit}',
                            f'{self.name} per {o.name}',
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
                self.unit = f'{self._unit}{self.supers[self.index]}'
            elif self.index < 100:
                t, u = divmod(self.index, 10)
                self.unit = f'{self._unit}{self.supers[t]}{self.supers[u]}'
            else:
                self.unit = f'{self._unit}^{self.index}'
        else:
            self.unit = self._unit

    def _updateName(self):
        """
        Our unit changed to have an exponent, update our representation
        """
        if 1 <= self.index <= len(self.x_names):
            self.x_name = self.x_names[self.index]
        else:
            self.x_name = f'{self.index}th '

    def __repr__(self) -> str:
        return f'{self.x_name}{self.name}'

    def __str__(self) -> str:
        return self.unit

    def convert(self, to: 'Unit', value: Union[float, int]) -> Union[float, int]:
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
        return Unit('', '')


# Empty Unit
NoUnit = Unit.NoUnit()


def get_units() -> tuple:
    """
    Get all the units
    :return:
    """
    return tuple(MetaUnit.unit_index.keys())


def get_all_conversions() -> dict:
    return MetaUnit.conversions


def get_all_divided_units() -> dict:
    return MetaUnit.divided_units


def get_all_combined_units() -> dict:
    return MetaUnit.combined_units


def get_unit(unitName) -> Unit:
    return MetaUnit.unit_index[unitName]


def get_combined_unit(unit) -> Unit:
    return MetaUnit.combined_units[unit]


def get_conversion(units):
    return MetaUnit.conversions.get(units)


def get_divided_unit(unit) -> Unit:
    return MetaUnit.divided_units[unit]


def has_unit(unit_id: str) -> bool:
    return unit_id in MetaUnit.unit_index


def has_combined_unit(unit_id) -> bool:
    return unit_id in MetaUnit.combined_units


def has_conversion(units) -> bool:
    return units in MetaUnit.conversions


def has_divided_unit(units) -> bool:
    return units in MetaUnit.divided_units
