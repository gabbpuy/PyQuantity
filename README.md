# PyQuantity
A library to deal with quantities, that have units. Quantities reduce themselves to the lowest SI prefix, see
Units.RealWorld to configure prefixes that aren't normally used.

## Usage
<pre>
<code lang=python>
>>> import PyQuantity.Quantity as Quantity
>>> import PyQuantity.Unit.Units as Units 
>>> 
>>> length = Quantity.Quantity(5, Units.metre)
>>> width = Quantity.Quantity(4,  Units.metre)
>>> area = length * width
>>> print area
20.0 m²
>>> area / length
4.0 m
</code>
</pre>
