# -*- coding: utf-8 -*-
import unittest

import quantity.unit.units as units
import quantity.prefix.prefixes as prefixes
import quantity.quantity as quantity


class TestQuantity(unittest.TestCase):

    def testSimpleQuantity(self):
        v = quantity.Quantity(3)
        assert v == 3

        y = quantity.Quantity(3)
        assert v == y

        z = quantity.Quantity(4)
        assert z != y
        assert v < z
        assert z > v
        assert y >= v
        assert v <= y

        v = quantity.Quantity(3, prefix=prefixes.kilo)
        assert v != y
        assert v == 3000
        assert v != 3

    def testQuantityMath(self):
        a = quantity.Quantity(3)
        b = quantity.Quantity(4)

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
        v10 = quantity.Quantity(10, 'V')
        a10 = quantity.Quantity(10, 'A')
        a20 = quantity.Quantity(20, 'A')
        v10_2 = quantity.Quantity(10, 'V')

        # Different units don't equal each other
        assert v10 != a10, (v10, a10)
        assert a10 != a20
        assert v10 != a20
        assert v10 == v10_2

    def testQuantityUnitMath(self):
        a = quantity.Quantity(10, 'V')
        b = quantity.Quantity(10, 'A')

        # This should make a new value with new units (Watts)
        c = a * b

        # Can we compare against a string unit
        assert c == quantity.Quantity(100, 'W'), (c,)

        # Can we compare against the explicit unit
        assert c == quantity.Quantity(100, units.watt)

        # It should commute
        assert a * b == b * a

        # Same units
        d = quantity.Quantity(50, 'W')
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
        mv3 = quantity.Quantity(3, 'MV')
        assert mv3.amount == 3.0
        assert mv3.unit is units.volt
        assert mv3.prefix is prefixes.mega, (mv3.prefix, prefixes.mega)

        # 3000 kilovolts should really be 3 megavolts
        mv3_2 = quantity.Quantity(3, 'kV', prefixes.kilo)
        assert mv3_2.amount == 3.0
        assert mv3_2.prefix is prefixes.mega

        # And they should be equal
        assert mv3 == mv3_2
