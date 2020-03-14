# -*- coding: utf-8 -*-
import unittest

from quantity.unit import Unit, has_unit
import quantity.unit.units as units


class TestUnit(unittest.TestCase):
    def testSimpleUnit(self):
        t = Unit('ZZZ', 'TestUnit', temp = True)
        assert not has_unit('ZZZ')

        t = Unit('ZZZ', 'TestUnit', False)
        assert has_unit('ZZZ')

    def testAddition(self):
        assert units.volt + units.volt is units.volt
        self.assertRaises(AssertionError, units.volt.__add__, units.ohm)
        self.assertRaises(AssertionError, units.volt.__add__, units.NoUnit)

    def testSubtraction(self):
        assert units.ampere - units.ampere is units.ampere
        self.assertRaises(AssertionError, units.ohm.__sub__, units.volt)
        self.assertRaises(AssertionError, units.ohm.__sub__, units.NoUnit)

    def testDivision(self):
        assert units.ampere / units.ampere is units.NoUnit
        assert units.ampere / units.NoUnit is units.ampere

    def testCombinedDivision(self):
        # Do we collapse the units?
        assert units.volt / units.ohm is units.ampere

        # This should make a temporary unit, as division is not commutative
        x = units.ohm / units.volt
        assert not has_unit(x)

    def testMultiplication(self):
        assert units.NoUnit * units.watt is units.watt
        assert units.watt * units.NoUnit is units.watt
        assert units.NoUnit * units.NoUnit is units.NoUnit

        w2 = units.watt * units.watt
        assert w2._unit is units.watt._unit
        assert w2.name is units.watt.name
        assert w2.index is 2

    def testCombinedMultiplication(self):
        # Do we make the special units?
        assert units.ampere * units.volt is units.watt
        # Do they commute?
        assert units.volt * units.ampere is units.watt
