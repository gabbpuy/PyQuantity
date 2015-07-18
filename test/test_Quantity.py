# -*- coding: utf-8 -*-
import unittest

import PyQuantity.Unit as Unit
import PyQuantity.Prefix as Prefix
import PyQuantity.Quantity as Quantity

Prefixes = Prefix.Prefixes
Units = Unit.Units


class TestQuantity(unittest.TestCase):

    def testSimpleQuantity(self):
        v = Quantity.Quantity(3)
        assert v == 3

        y = Quantity.Quantity(3)
        assert v == y

        z = Quantity.Quantity(4)
        assert z != y
        assert v < z
        assert z > v
        assert y >= v
        assert v <= y

        v = Quantity.Quantity(3, prefix = Prefixes.kilo)
        assert v != y
        assert v == 3000
        assert v != 3

    def testQuantityMath(self):
        a = Quantity.Quantity(3)
        b = Quantity.Quantity(4)

        c = a + b
        assert c == 7

        # Commute
        assert a + b == b + a

        c = a * b
        assert c == 12
        assert c / b == 3

        assert a * b == b * a

        assert b - a == 1.0
        assert a - b == -1.0, (a, b, a - b)

        # No commute
        assert a - b != b - a

    def testQuantityUnits(self):
        v10 = Quantity.Quantity(10, 'V')
        a10 = Quantity.Quantity(10, 'A')
        a20 = Quantity.Quantity(20, 'A')
        v10_2 = Quantity.Quantity(10, 'V')

        # Different units don't equal each other
        assert v10 != a10, (v10, a10)
        assert a10 != a20
        assert v10 != a20
        assert v10 == v10_2

    def testQuantityUnitMath(self):
        a = Quantity.Quantity(10, 'V')
        b = Quantity.Quantity(10, 'A')

        # This should make a new value with new units (Watts)
        c = a * b

        # Can we compare against a string unit
        assert c == Quantity.Quantity(100, 'W'), (c,)

        # Can we compare against the explicit unit
        assert c == Quantity.Quantity(100, Units.watt)

        # It should commute
        assert a * b == b * a

        # Same Units
        d = Quantity.Quantity(50, 'W')
        assert d < c
        assert d <= c
        assert c > d
        assert c >= d
        assert c != d

        # Can we do math?
        assert c - d == d
        assert d + d == c

        # It should commute
        assert c + d == d + c

        # Can we multiply by a scalar?
        assert d * 2 == c
        # Rmult
        assert 2 * d == c

        # Can we divide by a scalar?
        assert c / 2 == d
        assert a * b == d * 2

    def testQuantityPrefixUnit(self):
        # 3 megavolts
        mv3 = Quantity.Quantity(3, 'MV')
        assert mv3.amount == 3.0
        assert mv3.unit is Units.volt
        assert mv3.prefix is Prefixes.mega, (mv3.prefix, Prefixes.mega)

        # 3000 kilovolts should really be 3 megavolts
        mv3_2 = Quantity.Quantity(3, 'kV', Prefixes.kilo)
        assert mv3_2.amount == 3.0
        assert mv3_2.prefix is Prefixes.mega

        # And they should be equal
        assert mv3 == mv3_2
