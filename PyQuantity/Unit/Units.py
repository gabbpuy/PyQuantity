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
__author__ = 'akm'

import operator

from .Unit import NoUnit, Unit, getAllConversions, getAllDividedUnits, getAllCombinedUnits

# SI Base units
metre = Unit(u'm', u"metre")           # : SI metre
# Replace kilogramme with gramme because kg is a special case
# kilogramme = Unit.Unit('kg', 'kilogramme')
gramme = Unit(u'g', u"gramme")         # : SI grammes
second = Unit(u's', u"second")         # : SI seconds
ampere = Unit(u'A', u"ampere")         # : SI amperes
kelvin = Unit(u'K', u"kelvin")         # : SI kelvin
celsius = Unit(u"\u00b0C", u"celsius") # : SI celsius
mole = Unit(u"mol", u"mole")           # : SI mole
candela = Unit(u"cd", u"candela")      # : SI candela
steradian = Unit(u"sr", u"steradian")  # : SI steradian
radian = Unit(u"rad", u"radian")       # : SI radian
degree = Unit(u"\u00b0", u"degree")    # : degree of arc

hertz = Unit(u"Hz", u"hertz")          # : SI hertz
newton = Unit(u'N', u"newton")         # : SI newtons
pascal = Unit(u"Pa", u"pascal")        # : SI pascals
watt = Unit(u'W', u"watt")             # : SI watts
joule = Unit(u'J', u"joule")           # : SI joules
volt = Unit(u'V', u"volt")             # : SI volts
ohm = Unit(u"\u2126", u"ohm")          # : SI ohms (with omega symbol)
siemens = Unit(u'S', u"siemens")       # : SI siemens
coulomb = Unit(u'C', u"coulomb")       # : SI coulombs
farad = Unit(u'F', u"farad")           # : SI farads
weber = Unit(u"wb", u"weber")          # : SI weber
tesla = Unit(u"T", u"tesla")           # : SI tesla
henry = Unit(u'H', u"henry")           # : SI henrys
lumen = Unit(u"lm", u"lumen")          # : SI lumens
lux = Unit(u"lx", u"lux")              # : SI lux
becquerel = Unit(u"Bq", u"becquerel")  # : SI becquerel
gray = Unit(u"Gy", u"gray")            # : SI grays
sievert = Unit(u"Sv", u"sievert")      # : SI sieverts
katal = Unit(u"kat", u"katal")         # : SI katal

bit = Unit(u'b', u"bit")
byte = Unit(u'B', u"Byte")

# Non-English english aliases
meter = metre  #: SI alias for metre
gram = gramme  #: SI alias for gramme

# Imperial measurements
fahrenheit = Unit(u"\u00b0F", u"fahrenheit") # degrees fahrenheit
inch = Unit(u'"', u"inch")    # inch
foot = Unit(u"'", u"foot")    # foot
mile = Unit(u"mile", u"mile") # mile
pound = Unit(u"lb", u"pound") # pound
ounce = Unit(u"oz", u"ounce") # ounce

## Convenience conversions
minute = Unit(u"min", u"minute")
hour = Unit(u"hour", u"hour")

# One unit times another
# frozenset allows us to have commutative keys instead of doubling up each
# combination, so Amps * Volts and Volts * Amps both work off the same key
k = frozenset
getAllCombinedUnits().update({
    k((ampere, volt)): watt,
    k((ohm, ampere)): volt,
    k((second, ampere)): coulomb,
    k((second, watt)): joule,
    k((coulomb, volt)): joule,
    k((candela, steradian)): lumen,
    k((ohm, second)): henry,

##	k((metre, Newton))  : Joule, # or Newton-metres ...
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
getAllDividedUnits().update({
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

getAllConversions().update({
    (celsius, kelvin): ((operator.add, 273.15),),
    (kelvin, celsius): ((operator.sub, 273.15),),
    (celsius, fahrenheit): ((operator.mul, 9.0), (operator.div, 5.0), (operator.add, 32.0)),
    (fahrenheit, celsius): ((operator.sub, 32.0), (operator.mul, 5.0), (operator.div, 9.0)),
    (second, minute): ((operator.mul, 60.0),),
    (minute, second): ((operator.div, 60.0),),
    (second, hour): ((operator.mul, 3600.0),),
    (hour, second): ((operator.div, 3600.0),),
    (minute, hour): ((operator.mul, 60.0),),
    (hour, minute): ((operator.div, 60.0),),
    (inch, foot): ((operator.div, 12.0),),
    (foot, inch): ((operator.mul, 12.0),),
    (inch, metre): ((operator.mul, 0.0254),),
    (metre, inch): ((operator.mul, 39.3701),),
    (foot, metre): ((operator.mul, 0.3048),),
    (metre, foot): ((operator.mul, 3.28084),),
    (mile, foot): ((operator.mul, 5280.0),),
    (foot, mile): ((operator.div, 5280.0),),
    (mile, metre): ((operator.mul, 1609.34),),
    (metre, mile): ((operator.div, 1609.34),),
    (pound, gramme): ((operator.mul, 453.592),),
    (gramme, pound): ((operator.mul, 0.00220462),),
    (gramme, ounce): ((operator.mul, 0.035274),),
    (ounce, gramme): ((operator.mul, 28.3495),),
    (ounce, pound): ((operator.div, 16.0),),
    (pound, ounce): ((operator.mul, 16.0),),
    (bit, byte): ((operator.mul, 8.0),),
    (byte, bit): ((operator.div, 8.0),)
})