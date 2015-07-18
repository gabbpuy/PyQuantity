# -*- coding: utf-8 -*-
import unittest

import PyQuantity.Unit as Unit
Units = Unit.Units


class TestUnit(unittest.TestCase):
    def testSimpleUnit(self):
        t = Unit.Unit('ZZZ', 'TestUnit', True)
        assert not Unit.hasUnit('ZZZ')

        t = Unit.Unit('ZZZ', 'TestUnit', False)
        assert Unit.hasUnit('ZZZ')

    def testAddition(self):
        assert Units.volt + Units.volt is Units.volt
        self.assertRaises(AssertionError, Units.volt.__add__, Units.ohm)
        self.assertRaises(AssertionError, Units.volt.__add__, Units.NoUnit)

    def testSubtraction(self):
        assert Units.ampere - Units.ampere is Units.ampere
        self.assertRaises(AssertionError, Units.ohm.__sub__, Units.volt)
        self.assertRaises(AssertionError, Units.ohm.__sub__, Units.NoUnit)

    def testDivision(self):
        assert Units.ampere / Units.ampere is Units.NoUnit
        assert Units.ampere / Units.NoUnit is Units.ampere

    def testCombinedDivision(self):
        # Do we collapse the units?
        assert Units.volt / Units.ohm is Units.ampere

        # This should make a temporary unit, as division is not commutative
        x = Units.ohm / Units.volt
        assert not Unit.hasUnit(x)

    def testMultiplication(self):
        assert Units.NoUnit * Units.watt is Units.watt
        assert Units.watt * Units.NoUnit is Units.watt
        assert Units.NoUnit * Units.NoUnit is Units.NoUnit

        w2 = Units.watt * Units.watt
        assert w2._unit is Units.watt._unit
        assert w2.name is Units.watt.name
        assert w2.index is 2

    def testCombinedMultiplication(self):
        # Do we make the special units?
        assert Units.ampere * Units.volt is Units.watt
        # Do they commute?
        assert Units.volt * Units.ampere is Units.watt
