# -*- coding: utf-8 -*-
import unittest

import PyQuantity.Prefix as Prefix


class TestPrefix(unittest.TestCase):

    def testSimplePrefix(self):
        r = Prefix.closestPrefix(1000)
        assert r == (1.0, Prefix.Prefixes.kilo)

    def testComplexPrefix(self):
        r = Prefix.closestPrefix(1024)
        assert r == (1.024, Prefix.Prefixes.kilo)

    def testNegativePrefix(self):
        r = Prefix.closestPrefix(-1000)
        assert r == (-1.0, Prefix.Prefixes.kilo), r

    def testSmallPrefix(self):
        r = Prefix.closestPrefix(0.05)
        assert r == (50, Prefix.Prefixes.milli)

    def testScalarMult(self):
        assert Prefix.Prefixes.kilo * 5 == 5000

    def testScalarRightMult(self):
        assert 5 * Prefix.Prefixes.kilo == 5000
