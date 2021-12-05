# -*- coding: utf-8 -*-
"""
Predefined units of measure. Kilogramme has been replaced with gramme to make implementation easier
('kg' unit is still derivable using the prefix library)

The following units are also derivable:
(these commute)
Ampere * Volt   -> Watt
Ohm * Ampere    -> Volt
second * Ampere -> Coulomb

Watt / Ampere    -> Volt
Watt / Volt      -> Ohm
Volt / Ampere    -> Ohm
Volt / Ohm       -> Ampere
Coulomb / Ampere -> Farad
Ampere / Volt    -> Siemens
Joule / Ampere   -> Weber

You can use clever grouping to derive others e.g.
Power = (I^2)R = R(I^2)
Ohm * Ampere * Ampere -> Volt * Ampere -> Watt
Ampere * (Ampere * Ohm) -> Ampere * Volt -> Watt
"""
import operator

from .unit import Unit, get_all_conversions, get_all_divided_units, get_all_combined_units

# SI Base units
metre = Unit('m', "metre")  # : SI metre
# Replace kilogramme with gramme because kg is a special case
# kilogramme = Unit.Unit('kg', 'kilogramme')
gramme = Unit('g', "gramme")  # : SI grammes
second = Unit('s', "second")  # : SI seconds
ampere = Unit('A', "ampere")  # : SI amperes
kelvin = Unit('K', "kelvin")  # : SI kelvin
celsius = Unit("\u00b0C", "celsius")  # : SI celsius
mole = Unit("mol", "mole")  # : SI mole
candela = Unit("cd", "candela")  # : SI candela
steradian = Unit("sr", "steradian")  # : SI steradian
radian = Unit("rad", "radian")  # : SI radian
degree = Unit("\u00b0", "degree")  # : degree of arc

hertz = Unit("Hz", "hertz")  # : SI hertz
newton = Unit('N', "newton")  # : SI newtons
pascal = Unit("Pa", "pascal")  # : SI pascals
watt = Unit('W', "watt")  # : SI watts
joule = Unit('J', "joule")  # : SI joules
volt = Unit('V', "volt")  # : SI volts
ohm = Unit("\u2126", "ohm")  # : SI ohms (with omega symbol)
siemens = Unit('S', "siemens")  # : SI siemens
coulomb = Unit('C', "coulomb")  # : SI coulombs
farad = Unit('F', "farad")  # : SI farads
weber = Unit("wb", "weber")  # : SI weber
tesla = Unit("T", "tesla")  # : SI tesla
henry = Unit('H', "henry")  # : SI henrys
lumen = Unit("lm", "lumen")  # : SI lumens
lux = Unit("lx", "lux")  # : SI lux
becquerel = Unit("Bq", "becquerel")  # : SI becquerel
gray = Unit("Gy", "gray")  # : SI grays
sievert = Unit("Sv", "sievert")  # : SI sieverts
katal = Unit("kat", "katal")  # : SI katal

bit = Unit('b', "bit")
byte = Unit('B', "Byte")

# Non-English english aliases
meter = metre  #: SI alias for metre
gram = gramme  #: SI alias for gramme

# Imperial measurements
fahrenheit = Unit("\u00b0F", "fahrenheit")  # degrees fahrenheit
inch = Unit('"', "inch")  # inch
foot = Unit("'", "foot")  # foot
mile = Unit("mile", "mile")  # mile
pound = Unit("lb", "pound")  # pound
ounce = Unit("oz", "ounce")  # ounce

# Convenience conversions
minute = Unit("min", "minute")
hour = Unit("hour", "hour")

# One unit times another
# frozenset allows us to have commutative keys instead of doubling up each
# combination, so Amps * Volts and Volts * Amps both work off the same key
k = frozenset
get_all_combined_units().update({
    k((ampere, volt)): watt,
    k((ohm, ampere)): volt,
    k((second, ampere)): coulomb,
    k((second, watt)): joule,
    k((coulomb, volt)): joule,
    k((candela, steradian)): lumen,
    k((ohm, second)): henry,
    # k((metre, Newton))  : Joule, # or Newton-metres ...
})

# NB: we can only do pairs, and these are processed left to right.
# If you want e.g. W = (I ** 2)R you can multiply in the right order to get it
# e.g.
#
# W = R * I * I, OR
#     I * (I * R) or
#     I * R * I
#
# will give Watts, but,
#
# W = I * I * R
#
# will give  Square Ampere Ohms.
# We could make fake units to cope with this situation, but, not sure it's
# worth it right now.

# One unit divided by another
# tuples for keys means order is important for the key (which we want)
# See note above about order importance for creating the units you want.
get_all_divided_units().update({
    (watt, ampere): volt,
    (joule, coulomb): volt,
    (coulomb, volt): farad,
    (second, ohm): farad,
    (volt, ampere): ohm,
    (watt, volt): ohm,
    (volt, ohm): ampere,
    (ampere, volt): siemens,
    (joule, ampere): weber,
    (weber, ampere): henry,
    (joule, metre): newton,
    (joule, newton): metre,
    (joule, second): watt,
    (joule, gramme): sievert,
    (mole, second): katal
})

get_all_conversions().update({
    (celsius, kelvin): ((operator.add, 273.15),),
    (kelvin, celsius): ((operator.sub, 273.15),),
    # You can chain operators...
    (celsius, fahrenheit): ((operator.mul, 9.0), (operator.truediv, 5.0), (operator.add, 32.0)),
    (fahrenheit, celsius): ((operator.sub, 32.0), (operator.mul, 5.0), (operator.truediv, 9.0)),
    (second, minute): ((operator.mul, 60.0),),
    (minute, second): ((operator.truediv, 60.0),),
    (second, hour): ((operator.mul, 3600.0),),
    (hour, second): ((operator.truediv, 3600.0),),
    (minute, hour): ((operator.mul, 60.0),),
    (hour, minute): ((operator.truediv, 60.0),),
    (inch, foot): ((operator.truediv, 12.0),),
    (foot, inch): ((operator.mul, 12.0),),
    (inch, metre): ((operator.mul, 0.0254),),
    (metre, inch): ((operator.mul, 39.3701),),
    (foot, metre): ((operator.mul, 0.3048),),
    (metre, foot): ((operator.mul, 3.28084),),
    (mile, foot): ((operator.mul, 5280.0),),
    (foot, mile): ((operator.truediv, 5280.0),),
    (mile, metre): ((operator.mul, 1609.34),),
    (metre, mile): ((operator.truediv, 1609.34),),
    (pound, gramme): ((operator.mul, 453.592),),
    (gramme, pound): ((operator.mul, 0.00220462),),
    (gramme, ounce): ((operator.mul, 0.035274),),
    (ounce, gramme): ((operator.mul, 28.3495),),
    (ounce, pound): ((operator.truediv, 16.0),),
    (pound, ounce): ((operator.mul, 16.0),),
    (bit, byte): ((operator.truediv, 8.0),),
    (byte, bit): ((operator.mul, 8.0),)
})
