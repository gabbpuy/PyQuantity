# -*- coding: utf-8 -*-
__author__ = 'akm'
from .Prefix import Prefix

# A flag to remove some of the prefixes we don't like to use
RealWorld = True

NoPrefix = Prefix('', '', 0)             # : No Prefix
yotta = Prefix(u'Y', u'yotta', 24)       # : SI yotta
zetta = Prefix(u'Z', u'zetta', 21)       # : SI zetta
exa = Prefix(u'E', u'exa', 18)           # : SI exa
peta = Prefix(u'P', u'peta', 15)         # : SI peta
tera = Prefix(u'T', u'tera', 12)         # : SI tera
giga = Prefix(u'G', u'giga', 9)          # : SI giga
mega = Prefix(u'M', u'mega', 6)          # : SI mega
kilo = Prefix(u'k', u'kilo', 3)          # : SI kilo

if not RealWorld:
    # These prove to be difficult in "the real world"
    # hecto is commonly used with Pascals though
    # ditto deca for steradians
    # ditto deci for litres
    # ditto centi for metres
    hecto = Prefix(u'h', u'hecto', 2)    # : SI hecto (needs RealWorld = False)
    deca = Prefix(u'da', u'deca', 1)     # : SI deca (needs RealWorld = False)
    deci = Prefix(u'd', u'deci', -1)     # : SI deci (needs RealWorld = False)
    centi = Prefix(u'c', u'centi', -2)   # : SI centi (needs RealWorld = False)

milli = Prefix(u'm', u'milli', -3)       # : SI milli
micro = Prefix(u'u', u'micro', -6)       # : SI micro
# We want this to be the one, so we do it 2nd so it ends up in the index
micro = Prefix(u'\u00B5', u'micro', -6)  # : SI micro (with mu symbol)
nano = Prefix(u'n', u'nano', -9)         # : SI nano
pico = Prefix(u'p', u'pico', -12)        # : SI pico
femto = Prefix(u'f', u'femto', -15)      # : SI femto
atto = Prefix(u'a', u'atto', -18)        # : SI atto
zepto = Prefix(u'z', u'zepto', -21)      # : SI zepto
yocto = Prefix(u'y', u'yocto', -24)      #: SI yocto

