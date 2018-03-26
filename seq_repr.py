"""
Some sequence representation classes

1. by difference [1, 2, 3, 4] -- > (1, [1, 1, 1])
2. by digits [12, 23, 34, 45] -- > [[1, 2], [2, 3], [3, 4], [4, 5]]

"""
from helper import sign, iter_pairs
__all__ = ("AlterRepr", "DiffRepr", "NormalRepr", "AbsRepr", "RatioRepr",
           "DivModRepr", "DivModRepr2")


class Representation:
    """ Base class for representing sequences """
    @classmethod
    def isConsidering(cls, seq):
        """ Check if this representation worth considering for this sequence
        """
        return True


class NormalRepr(list, Representation):
    """ Normal sequence representation """

    def __repr__(self):
        return list.__repr__(self)

    def readable(self):
        """ [1, 2, 3, 4] --> "1, 2, 3, 4" """
        return ", ".join(map(str, self))

    def __add__(self, other):
        if type(other) in (int, float):
            seq = [i + other for i in self]
            return NormalRepr(seq)
        return super().__add__(other)

    def __sub__(self, other):
        if type(other) in (int, float):
            seq = [i - other for i in self]
            return NormalRepr(seq)
        else:
            seq = [i - j for i, j in zip(reversed(self), reversed(other))]
            return NormalRepr(seq)

    def __mul__(self, other):
        seq = [i * other for i in self]
        return NormalRepr(seq)

    def __rmul__(self, other):
        seq = [i * other for i in self]
        return NormalRepr(seq)

    def __radd__(self, other):
        seq = [i + other for i in self]
        return NormalRepr(seq)

    def __div__(self, other):
        seq = [i / other for i in self]
        return NormalRepr(seq)

    def reversed_copy(self):
        """ Return a reversed copy of the sequence """
        return self.__class__([self[::-1]])

    def is_constant(self):
        it = iter(self)
        first = next(it)
        for i in it:
            if i != first:
                return False
        return True


class AlterRepr(Representation):
    """ [1, 2, 3, 4, 5] --> ([1, 3, 5], [2, 4]) """
    @classmethod
    def convert(cls, seq):
        size = len(seq)
        evens = NormalRepr([seq[2 * i] for i in range((size + 1) // 2)])
        odds = NormalRepr([seq[2 * i + 1] for i in range(size // 2)])
        return AlterRepr(odds=odds, evens=evens)

    def __init__(self, odds, evens):
        self.odds = odds
        self.evens = evens

    def toNormal(self):
        normal = NormalRepr([])
        for i in range(len(self.evens)):
            try:
                normal.append(self.evens[i])
                normal.append(self.odds[i])
            except IndexError:
                pass
        return normal

    def __repr__(self):
        return "<AlterRepr ({}, {})>".format(self.evens, self.odds)


class AbsRepr(Representation):
    """- seperated signs and absolute values
    Example: (1, -1, 1, -1), (1, 2, 3, 4) --> 1, -2, 3, -4,
    Attributes:
        signs: a list of {-1, 0, 1} representing signs of sequence terms
        values: positive(absolute) values of sequence
    """
    @classmethod
    def isConsidering(cls, seq):
        """ Check if this representation worth considering for this sequence
        """
        if not any(i < 0 for i in seq):
            return False

        signs = [sign(i) for i in seq]
        if all(i == j for i, j in zip(signs, seq)):
            return False
        values = NormalRepr([abs(i) for i in seq])
        if all(i == j for i, j in zip(values, seq)):
            return False

        return super().isConsidering(seq)

    @classmethod
    def convert(cls, seq):
        """ Return AbsRepr for seq """
        signs = NormalRepr([sign(i) for i in seq])
        values = NormalRepr([abs(i) for i in seq])
        return AbsRepr(signs=signs, values=values)

    def __init__(self, signs, values):
        self.signs = signs
        self.values = values

    def toNormal(self):
        return NormalRepr([s * v for s, v in zip(self.signs, self.abs_values)])

    def __repr__(self):
        return "<AlterRepr ({} with signs {})>".format(self.abs_values,
                                                       self.signs)


class DiffRepr(Representation):
    @classmethod
    def convert(cls, seq):
        first = seq[0]
        differences = NormalRepr([num - prev_num for prev_num, num in iter_pairs(seq)])
        return DiffRepr(first, differences)

    def __init__(self, first, differences):
        self.first = first
        self.differences = differences

    def toNormal(self):
        """ Return normal representation of the seq """
        last = self.first
        normal = NormalRepr([last])
        for d in self.differences:
            last += d
            normal.append(last)
        return normal

    def __repr__(self):
        return "<DiffRepr ({}, {})>".format(self.first, self.differences)


class RatioRepr(Representation):
    @classmethod
    def isConsidering(cls, seq):
        try:
            for i, ii in iter_pairs(seq):
                if ii % i != 0:
                    return False
            return True
        except ZeroDivisionError:
            return False

    @classmethod
    def convert(cls, seq):
        first = seq[0]
        ratios = NormalRepr([round(seq[i] / seq[i-1]) for i in range(1, len(seq))])
        return RatioRepr(first, ratios)

    def __init__(self, first, ratios):
        self.first = first
        self.ratios = ratios

    def toNormal(self):
        """ Return normal representation of the seq """
        last = self.first
        normal = NormalRepr([last])
        for d in self.ratios:
            last *= d
            normal.append(last)
        return normal

    def __repr__(self):
        return "<RatioRepr ({}, {})>".format(self.first, self.ratios)


class DivModRepr(Representation):
    @classmethod
    def isConsidering(cls, seq):
        if any(i == 0 or type(i) != int for i in seq):
            return False
        return super().isConsidering(seq)

    def __init__(self, normal):
        self.first = normal[0]
        self.divs = NormalRepr([])
        self.mods = NormalRepr([])
        for i, ii in iter_pairs(normal):
            div, mod = divmod(ii, i)
            self.divs.append(div)
            self.mods.append(mod)

    def toNormal(self):
        si = self.first
        normal = NormalRepr([si])
        for div, mod in zip(self.divs, self.mods):
            si = si * div + mod
            normal.append(si)
        return normal

    def __repr__(self):
        return "<DivModRepr (first={}, divs={}, mods={})>".format(self.first,
                                                                  self.divs,
                                                                  self.mods)


class DivModRepr2(DivModRepr):
    def __init__(self, normal):
        self.first = normal[0]
        self.divs = NormalRepr([])
        self.mods = NormalRepr([])
        for i, ii in iter_pairs(normal):
            div, mod = divmod(ii, i)
            self.divs.append(div + 1)
            self.mods.append(mod - i)


if __name__ == "__main__":
    s = NormalRepr([8, 6, 9, 23, 87])
    dm = DivModRepr2(s)
    print(dm)
    print(dm.toNormal())
