# -*- coding: utf-8 -*-
import unittest

import quantity.prefix.prefix as prefix
import quantity.prefix.prefixes as prefixes


class TestPrefix(unittest.TestCase):

    def test_simple_prefix(self):
        r = prefix.closest_prefix(1000)
        assert r == (1.0, prefixes.kilo)

    def test_complex_prefix(self):
        r = prefix.closest_prefix(1024)
        assert r == (1.024, prefixes.kilo)

    def test_negative_prefix(self):
        r = prefix.closest_prefix(-1000)
        assert r == (-1.0, prefixes.kilo), r

    def test_small_prefix(self):
        r = prefix.closest_prefix(0.05)
        assert r == (50, prefixes.milli)

    def test_scalar_multiply(self):
        assert prefixes.kilo * 5 == 5000

    def test_scalar_right_multiply(self):
        assert 5 * prefixes.kilo == 5000
