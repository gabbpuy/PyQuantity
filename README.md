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
Unit.Units defines SI units, which are looked up by symbol.

<pre>
<code lang=python>
>>> q = Quantity(1.0, "MV")
>>> q
1.0 MV
>>> q = Quantity(1000000, 'V')
>>> q
1.0 MV
>>> q.to('V')
1000000.0
</code>
</pre>
Many simple conversions are also provided

<pre>
<code lang=python>
>>> volts = Quantity(10, 'V')
>>> amps = Quantity(100, 'A')
>>> volts * amps
1.0 kW
>>> volts / amps
100.0 mΩ
</code>
</pre>
You can define your own units. We can get frames per second by defining frames.

<pre>
<code lang=python>
>>> frame = Unit.Unit('f', "frame")
>>> frames = Quantity(432000, "frame")
>>> runningTime = Quantity(120 * 60, 's')
>>> fps = frames / runningTime
>>> fps
60.0 f/s
</code>
</python>
