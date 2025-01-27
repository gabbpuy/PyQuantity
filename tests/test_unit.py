# -*- coding: utf-8 -*-
import unittest

from quantity.unit import Unit, has_unit
from quantity.unit import NoUnit
import quantity.unit.units as units


class TestUnit(unittest.TestCase):
    def test_simple_unit(self):
        t = Unit('ZZZ', 'TestUnit', temp=True)
        assert not has_unit('ZZZ')

        t = Unit('ZZZ', 'TestUnit', False)
        assert has_unit('ZZZ')

    def test_addition(self):
        assert units.volt + units.volt is units.volt
        self.assertRaises(AssertionError, units.volt.__add__, units.ohm)
        self.assertRaises(AssertionError, units.volt.__add__, NoUnit)

    def test_subtraction(self):
        assert units.ampere - units.ampere is units.ampere
        self.assertRaises(AssertionError, units.ohm.__sub__, units.volt)
        self.assertRaises(AssertionError, units.ohm.__sub__, NoUnit)

    def test_division(self):
        assert units.ampere / units.ampere is NoUnit
        assert units.ampere / NoUnit is units.ampere

    def test_combined_division(self):
        # Do we collapse the units?
        assert units.volt / units.ohm is units.ampere

        # This should make a temporary unit, as division is not commutative
        x = units.ohm / units.volt
        assert not has_unit(x)

    def test_multiplication(self):
        assert NoUnit * units.watt is units.watt
        assert units.watt * NoUnit is units.watt
        assert NoUnit * NoUnit is NoUnit

        w2 = units.watt * units.watt
        assert w2._unit is units.watt._unit
        assert w2.name is units.watt.name
        assert w2.index == 2

    def test_combined_multiplication(self):
        # Do we make the special units?
        assert units.ampere * units.volt is units.watt
        # Do they commute?
        assert units.volt * units.ampere is units.watt
