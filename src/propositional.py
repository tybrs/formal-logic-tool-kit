from prettytable import PrettyTable
from itertools import product


class Atom:

    def __init__(self, var_name: str, truth_value=None):

        self.truth_value = truth_value

        self.var_name = self.get_varname(var_name)

        self.symbol = 'α'

    def __repr__(self):
        if self.truth_value is not None:
            return '{}={}'.format(self.var_name, self.truth_value)
        else:
            return self.var_name

    def __iter__(self):
        yield self

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __gt__(self, other):
        return IfThen(self, other)

    def __invert__(self):
        return Not(self)

    def __bool__(self):
        return self.truth_value

    def __lt__(self, other):
        return self.var_name < other.var_name

    def __eq__(self, other):
        if self.truth_value is not None:
            return self.truth_value == other.truth_value

    def __hash__(self):
        return id(self.var_name)

    def copy(self):
        return Atom(self.var_name, truth_value=self.truth_value)

    def tree(self, dtype='list'):
        if dtype == 'list':
            return [self.symbol, self.var_name]
        elif dtype == 'str':
            return "[{} {}]".format(self.symbol, self.var_name)
        elif dtype == 'dict':
            return {'label': self.symbol, 'constituents': self.var_name}

    def get_atoms(self):
        return self

    def get_varname(self, var_name):
        if var_name.isalnum():
            return var_name.upper()
        else:
            raise ValueError('Only alphanumeric charachters can be atomic'
                             'propositions: "{}" not alpha.'.format(var_name))


class Formula:

    def __init__(self, phi):
        self.phi = phi
        self.psi = None
        self.atoms = sorted(self.get_atoms())

    def __bool__(self):
        return bool(self.phi)

    def __repr__(self):
        return repr(self.phi)

    def __iter__(self):
        yield self

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __gt__(self, other):
        return (IfThen(self, other))

    def __eq__(self, other):
        return Iff(self, other)

    def __invert__(self):
        return Not(self)

    def get_atoms(self):
        atoms = set()
        if isinstance(self.phi, Atom):
            atoms.add(self.phi)
        else:
            atoms.update(self.phi.get_atoms())

        if isinstance(self.psi, Atom):
            atoms.add(self.psi)
        elif self.psi is not None:
            atoms.update(self.psi.get_atoms())
        return atoms

    def replace_atoms(self, *atoms):
        for atom in atoms:
            replaced = self.replace_atom(atom)
        return replaced

    def replace_atom(self, atom):
        if isinstance(self.phi, Atom) and self.phi.var_name == atom.var_name:
            self.phi = atom
        if isinstance(self.psi, Atom) and self.psi.var_name == atom.var_name:
            self.psi = atom
        if isinstance(self.phi, Formula):
            self.phi.replace_atom(atom)
        if isinstance(self.psi, Formula):
            self.psi.replace_atom(atom)
        return self

    def truth_table(self):
        return TruthTable([self])

    def tree(self, dtype='list'):
        if dtype == 'list':
            return [self.symbol, self.phi.tree(dtype), self.psi.tree(dtype)]
        elif dtype == 'str':
            return "[{} {} {}]".format(self.symbol, self.phi.tree(dtype),
                                       self.psi.tree(dtype))
        elif dtype == 'dict':
            return {'label': self.symbol,
                    'constituents': [self.phi.tree(dtype),
                                     self.psi.tree(dtype)]}


class And(Formula):

    def __init__(self, phi: Formula, psi: Formula):
        self.n_ary = 2
        self.phi = phi
        self.psi = psi
        self.atoms = sorted(self.get_atoms())
        self.symbol = '&'

    def __repr__(self):
        return '({} {} {})'.format(repr(self.phi), self.symbol, repr(self.psi))

    def __bool__(self):
        return bool(self.phi) and bool(self.psi)

    def copy(self):
        return And(self.phi.copy(), self.psi.copy())


class Or(Formula):

    def __init__(self, phi: Formula, psi: Formula):
        self.n_ary = 2
        self.phi = phi
        self.psi = psi
        self.atoms = sorted(self.get_atoms())
        self.symbol = '∨'

    def __repr__(self):
        return '({} {} {})'.format(repr(self.phi), self.symbol, repr(self.psi))

    def __bool__(self):
        return bool(self.phi) or bool(self.psi)

    def copy(self):
        return Or(self.phi.copy(), self.psi.copy())


class IfThen(Formula):

    def __init__(self, phi: Formula, psi: Formula):
        self.n_ary = 2
        self.phi = phi
        self.psi = psi
        self.atoms = sorted(self.get_atoms())
        self.symobl = '🡢'

    def __repr__(self):
        return '({} {} {})'.format(repr(self.phi), self.symbol, repr(self.psi))

    def __bool__(self):
        return (not bool(self.phi)) or bool(self.psi)

    def copy(self):
        return IfThen(self.phi.copy(), self.psi.copy())


class Iff(Formula):

    def __init__(self, phi: Formula, psi: Formula):
        self.n_ary = 2
        self.phi = phi
        self.psi = psi
        self.atoms = sorted(self.get_atoms())
        self.symbol = '🡘'

    def __repr__(self):
        return '({} {} {})'.format(repr(self.phi), self.symbol, repr(self.psi))

    def __bool__(self):
        return (bool(self.phi) and bool(self.psi)) or \
            not(bool(self.phi) or bool(self.psi))

    def copy(self):
        return Iff(self.phi.copy(), self.psi.copy())


class Not(Formula):

    def __init__(self, phi: Formula):
        self.n_ary = 1
        self.phi = phi
        self.psi = None
        self.atoms = sorted(self.get_atoms())
        self.symbol = '¬'

    def __repr__(self):
        return '{}({})'.format(self.symbol, repr(self.phi))

    def __bool__(self):
        return not (bool(self.phi))

    def copy(self):
        return Not(self.phi.copy())

    def get_atoms(self):
        if isinstance(self.phi, Atom):
            return set(self.phi)
        else:
            return self.phi.get_atoms()

    def tree(self, dtype='list'):
        if dtype == 'list':
            return [self.symbol, self.phi.tree(dtype)]
        elif dtype == 'str':
            return "[{} {}]".format(self.symbol, self.phi.tree(dtype))
        elif dtype == 'dict':
            return {'label': self.symbol, 'constituents': self.phi.tree(dtype)}


class TruthTable:

    def __init__(self, formulas):
        self.formulas = formulas
        self.atoms = [Formula(phi).atoms for phi in formulas]
        self.universe = set.union(set(*self.atoms))
        self.universe = sorted(self.universe)
        self.truth_assignments = self.assign_truth()
        self.n_modles = len(self.truth_assignments)
        self.models = self.get_models()

    def get_models(self):
        models = []
        formulas = [formula.copy()
                    for formula in self.formulas * self.n_modles]
        zip_truths_form = list(zip(self.truth_assignments, formulas))
        for truths, formula in zip_truths_form:
            formula_in_m = formula.replace_atoms(*truths)
            models.append(formula_in_m)
        return models

    def get_tuth(self):
        return {atom: bool(atom) for atom in self.universe}

    def purm_truth(self):
        return product([True, False], repeat=len(self.universe))

    def assign_truth(self):
        model_values = list(self.purm_truth())
        models = [tuple(atom.copy() for atom in self.universe)
                  for value in model_values]
        for atoms, values in zip(models, model_values):
            for index, atom in enumerate(atoms):
                atom.truth_value = values[index]
        return models

    def __repr__(self):
        table = PrettyTable()

        table.field_names = [repr(phi) for phi in self.universe] + \
            [repr(phi) for phi in self.formulas]

        for atoms, formula in zip(self.truth_assignments, self.models):
            table.add_row([bool(phi) for phi in atoms] + [bool(formula)])
        return str(table)
