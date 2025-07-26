# -*- coding: utf-8 -*-
from functools import partial
from configparser import ConfigParser
from typing import Union, Callable, override

from quantity.quantity import Quantity
from quantity.unit import NoUnit

_hex = partial(int, base=16)


class QuantityConfigParser(ConfigParser):
    """
    A :mod:`SafeConfigParser` derivative that returns quantities
    """

    def get_as(self, section: str, option: str, converter: Callable) -> Quantity:
        """
        Convert a section to a coerced Quantity
        :param section: Config section
        :param option: Config option
        :param converter: callable that returns a numeric type from a string (e.g int, float )
        :return: :mod:`Quantity`
        """
        value, unit = self._split_section_item(section, option)
        return self.__quantify(converter, value, unit)

    @override
    def getint(self, section: str, option: str, converter: Callable = int) -> Quantity:
        """
        A convenience method which coerces the option in the specified
        section to an integer :mod:`Quantity`

        :param section: Config section
        :param option: Option of the section
        :param converter: a string to int callable
        :return: :mod:`Quantity`
        """
        return self.get_as(section, option, converter)

    def gethex(self, section: str, option: str, converter: Callable = _hex) -> Quantity:
        """
        A convenience method which coerces the option in the specified
        section to an integer :mod:`Quantity` from a hex input. Values
        can have a leading 0x or not.

        :param section: Config section
        :param option: Option of the section
        :param converter: a hex string to int callable
        :return: :mod:`Quantity`
        """
        return self.get_as(section, option, converter)

    @override
    def getfloat(self, section: str, option: str, converter: Callable = float) -> Quantity:
        """
        A convenience method which coerces the option in the specified
        section to a float :mod:`Quantity`

        :param section: Config section
        :param option: Option of the section
        :param converter: a string to float callable
        :return: :mod:`Quantity`
        """
        return self.get_as(section, option, converter)

    def _split_section_item(self, section: str, option: str) -> tuple:
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
            unit = NoUnit
        return value, unit

    @staticmethod
    def __quantify(converter: Callable, value: Union[float, int], unit: str) -> Quantity:
        """
        Return a type cast quantity

        :param converter: A conversion callable (i.e. int, float)
        :param value: The value (1, 1.0, 100)
        :param unit: The SI quantifier ('s', 'km')
        :returns: A :mod:`Quantity` object
        """
        return Quantity(converter(value), unit)
