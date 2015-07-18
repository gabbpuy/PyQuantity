# -*- coding: utf-8 -*-
from functools import partial
from ConfigParser import SafeConfigParser

import PyQuantity.Quantity as Quantity
import PyQuantity.Unit as Unit
Units = Unit.Units

_hex = partial(int, base = 16)


class QuantityConfigParser(SafeConfigParser):
    """
    A :mod:`SafeConfigParser` derivative that returns quantities
    """

    @staticmethod
    def __quantify(converter, value, unit):
        """
        Return a type cast quantity

        :param converter: A conversion callable (i.e. int, float)
        :param value: The value (1, 1.0, 100)
        :param unit: The SI quantifier ('s', 'km')
        :returns: A :mod:`Quantity` object
        """
        return Quantity.Quantity(converter(value), unit)

    def _splitSectionItem(self, section, option):
        """
        Split a config value into value and unit
        :param section: Config section
        :param option: Config option
        :return: :mod:`tuple` of value and unit
        """
        s = self.get(section, option)
        try:
            value, unit = (x.strip() for x in s.split(None, 1))
        except ValueError:
            value = s
            unit = Units.NoUnit
        return value, unit

    def getAs(self, section, option, converter):
        """
        Convert a section to a coerced Quantity
        :param section: Config section
        :param option: Config option
        :param converter: callable that returns a numeric type from a string (e.g int, float )
        :return: :mod:`Quantity`
        """
        value, unit = self._splitSectionItem(section, option)
        return self.__quantify(converter, value, unit)

    def getint(self, section, option, converter = int):
        """
        A convenience method which coerces the option in the specified
        section to an integer :mod:`Quantity`

        :param section: Config section
        :param option: Option of the section
        :param converter: a string to int callable
        :return: :mod:`Quantity`
        """
        return self.getAs(section, option, converter)

    def gethex(self, section, option, converter = _hex):
        """
        A convenience method which coerces the option in the specified
        section to an integer :mod:`Quantity` from a hex input. Values
        can have a leading 0x or not.

        :param section: Config section
        :param option: Option of the section
        :param converter: a hex string to int callable
        :return: :mod:`Quantity`
        """
        return self.getAs(section, option, converter)

    def getfloat(self, section, option, converter = float):
        """
        A convenience method which coerces the option in the specified
        section to a float :mod:`Quantity`

        :param section: Config section
        :param option: Option of the section
        :param converter: a string to float callable
        :return: :mod:`Quantity`
        """
        return self.getAs(section, option, converter)
