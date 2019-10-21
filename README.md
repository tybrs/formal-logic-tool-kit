# Formal Language Tool Kit

Programmatic interface for modeling propositional logic. Classes attempted to be written in a way that is both Pythonic and analogous to recursive model theoretic definitions.

# Propositional Logic

## Model
Model any well-formed formulas in propositional logic and compute its value:
```python
>>> p = Atom('P' True)
>>> q = Atom('Q', False)
>>> IfThen(And(IfThen(p, q), p), q)
(((P 🡢 Q) & P) 🡢 Q)
```
Or alternatively use operators between formula.
```
>>> bool(((P > Q) & P) > Q)
True
```
Or alternatively use operators between formula.
Compute truth-tables:

```
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

The following table shows modus ponens is logically equivalent to modus tollens.
```
>>> ((((P > Q) & P) > Q) == (((P > Q) & ~Q) > ~P)).truth_table()
+-------+-------+-----------------------------------------------------+
|   P   |   Q   | ((((P 🡢 Q) & P) 🡢 Q) 🡘 (((P 🡢 Q) & (¬Q)) 🡢 (¬P))) |
+-------+-------+-----------------------------------------------------+
|  True |  True |                        True                         |
|  True | False |                        True                         |
| False |  True |                        True                         |
| False | False |                        True                         |
+-------+-------+-----------------------------------------------------+
```


# TODO

* Write grammar for parser generator to translate formal logical syntax into FLTK `parse("P & Q")` returns `And(Atom(P), Atom(Q))`
* Write `Tableau` class and add more proof theoretic functionality
* Add `Argument` class.
* Add support for logical equivalence between formula
* Add module for predicate logic