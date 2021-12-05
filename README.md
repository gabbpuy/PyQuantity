# PyQuantity
A library to deal with quantities, that have units. Quantities reduce themselves to the lowest SI prefix, see
Units.RealWorld to configure prefixes that aren't normally used.

## Usage
```python
from quantity.quantity import Quantity
import quantity.unit.units as units 

length = Quantity(5, units.metre)
width = Quantity(4,  units.metre)
area = length * width
print(area)
'20.0 m²'
area / length
'4.0 m'
```

unit.units defines SI units, which are looked up by symbol.

```python
from quantity.quantity import Quantity

q = Quantity(1.0, "MV")
print(q)
'1.0 MV'
q = Quantity(1000000, 'V')
print(q)
'1.0 MV'
print(q.to('V'))
1000000.0
```

Many simple conversions are also provided

```python
from quantity.quantity import Quantity

volts = Quantity(10, 'V')
amps = Quantity(100, 'A')
volts * amps
'1.0 kW'
volts / amps
'100.0 mΩ'
```

You can define your own units. We can get frames per second by defining frames.

```python
from quantity.unit import Unit
from quantity.quantity import Quantity

frame = Unit('f', "frame")
frames = Quantity(432000, "frame")
running_time = Quantity(120 * 60, 's')
fps = frames / running_time
print(fps)
'60.0 f/s'
```
