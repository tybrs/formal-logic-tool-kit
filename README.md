# Formal Language Tool Kit

Progamatic interface for modeling propositional logic. Classes atempted to be writen in a way that is both pythonic and analogous to recursive model theortic definitions.

# Propositional Logic

## Model
Model any well-formed formulas in propositonal logic and compute its value:
```python
>>> p = Atom('P' Tr)
>>> q = Atom('Q', False)
>>> modus_ponens = IfThen(And(IfThen(p, q), p), q)
(((P 🡢 Q) & P) 🡢 Q)
>>> bool(modus_ponens)
True
```

Compute truth-tables:

```python
>>> Not(And(P, Q)).truth_table()
+-------+-------+------------+
|   P   |   Q   | (¬(P & Q)) |
+-------+-------+------------+
|  True |  True |   False    |
|  True | False |    True    |
| False |  True |    True    |
| False | False |    True    |
+-------+-------+------------+
```

# TODO

* Write grammar for parser generator to translate formal locigal syntax into FLTK `parse(P & Q)` And()
* Write tableau class and add more proof theoretic functionality
* Add `Argument` class.
* Add support for logical equivilience between formula
* Add module for predicate logic