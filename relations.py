"""
Relations module about integers.
"""


__all__ = ["SimpleRelations", "all_relations"]


class Relation():
    def __init__(self, name="[Relation]", arg_num=2, symmetric=False):
        self.arg_num = arg_num
        self.name = name

    def __call__(self, *args):
        if self.rel_func(*args) == 0:
            return True
        return False

    def amount(self, *args):
        pass


def isEqual(*args):
    j = args[0]
    for i in args:
        if i != j:
            return False
    return True


def isDivisible(a, b):
    return a % b == 0


def isDivisor(a, b):
    return b % a == 0


# Equality Relation and amount
def equality_amount(*args):
    if isEqual(*args):
        return 1
    return 0


RelEquality = Relation(name="Equal", arg_num=-1, symmetric=True)
RelEquality.amount = equality_amount


# Divisiblity Relation and amount
divams = {1: .1,
          2: .5,
          3: .7,
          4: .8,
          5: .9}


def divisiblity_amount(a, b):
    if a == 0:
        return 0.1
    if b == 0:
        return 0
    if a == b:
        return .1
    if a % b == 0:
        try:
            return divams[b]
        except KeyError:
            return 1
    return 0


RelDivisiblity = Relation(name="Divisible")
RelDivisiblity.amount = divisiblity_amount


all_relations = (RelDivisiblity, RelEquality)


def SimpleRelations(a, b, relation_list=all_relations):
    """Searches for simple relations between a and b a sorted list of (amount, r)
    sorted according to relativity amount"""
    res = []  # all tuples (amount, relation) sorted according to amount

    for r in all_relations:
        if r.arg_num in (2, -1):
            amount = r.amount(a, b)
            if amount > 0:
                res.append((amount, r))

    res = sorted(res, reverse=True)
    return res


if __name__ == "__main__":
    for am, r in SimpleRelations(2, 4):
        print(am, r.name)
