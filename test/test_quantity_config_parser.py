# -*- coding: utf-8 -*-
import os
import unittest

from quantity.quantity_config_parser import QuantityConfigParser

here = os.path.dirname(__file__)


class TestQuantityConfigParser(unittest.TestCase):
    """
    Test Quantity Config Parser
    """

    def setUp(self):
        with open(os.path.join(here, 'TestData', 'Test.ini'), 'rt', encoding='utf-8') as fp:
            qcp = QuantityConfigParser()
            qcp.read_file(fp)
            self.qcp = qcp

    def testGetInt(self):
        """
        Test Integer Fetching
        """
        v = self.qcp.getint('Ints', 'value1')
        assert int(v) == 120

        v = self.qcp.getint('Ints', 'value2')
        assert int(v.amount) == 50, int(v)

    def testGetFloat(self):
        """
        Test Float Fetching
        """
        # Get ints as floats
        v = self.qcp.getfloat('Ints', 'value1')
        assert v.amount == 120.0, v.amount

        v = self.qcp.getfloat('Ints', 'value2')
        assert v.amount == 50, v.amount

        v = self.qcp.getfloat('Floats', 'value1')
        assert v.amount == 50.0, v.amount

        v = self.qcp.getfloat('Floats', 'value2')
        assert round(abs(0.35 - v.amount), 2) == 0

    def testGetNoQualifier(self):
        """
        Testing items with no qualifiers
        """
        v = self.qcp.getint('NoUnits', 'value1')
        assert v == -5.0, (v,)

        v = self.qcp.getint('NoUnits', 'value2')
        assert v == 0, (v,)

    def testGetHex(self):
        """
        Test Hex Fetching
        """
        v = self.qcp.gethex('Hex', 'value1')
        assert v == 255

        v = self.qcp.gethex('Hex', 'value2')
        assert v == 0xDEADC0DE
