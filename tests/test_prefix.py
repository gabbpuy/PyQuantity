# -*- coding: utf-8 -*-
import unittest

import quantity.prefix.prefix as prefix
import quantity.prefix.prefixes as prefixes


class TestPrefix(unittest.TestCase):

    def testSimplePrefix(self):
        r = prefix.closest_prefix(1000)
        assert r == (1.0, prefixes.kilo)

    def testComplexPrefix(self):
        r = prefix.closest_prefix(1024)
        assert r == (1.024, prefixes.kilo)

    def testNegativePrefix(self):
        r = prefix.closest_prefix(-1000)
        assert r == (-1.0, prefixes.kilo), r

    def testSmallPrefix(self):
        r = prefix.closest_prefix(0.05)
        assert r == (50, prefixes.milli)

    def testScalarMult(self):
        assert prefixes.kilo * 5 == 5000

    def testScalarRightMult(self):
        assert 5 * prefixes.kilo == 5000
