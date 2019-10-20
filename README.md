# Formal Language Tool Kit

Progamatic interface fot modeling propositional logic with pythonic class custructions.

# Propositional Logic

## Model
```python
P = Atom('p', True)
Q = Atom('p', False)
IfThen(P, Q)
>>> (P 🡢 Q)
```

```python
bool(IfThen(P, Q))
>>> False
```

```python
Not(And(P, Q)).truth_table()
>>> +-------+-------+------------+
    |   P   |   Q   | (¬(P & Q)) |
    +-------+-------+------------+
    |  True |  True |   False    |
    |  True | False |    True    |
    | False |  True |    True    |
    | False | False |    True    |
    +-------+-------+------------+
```

# TODO

* Write grammar for parser generator to translate formal locigal syntax into FLTK
* Write tableau class and add more proof theoretic functionality
* Add support for logical equivilience between formula
* Add module for predicate logic