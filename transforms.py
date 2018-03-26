class SimpleTransform:
    """ Base class for transforms like increase, decrease, divide, multiply.
    Attributes:
        self.arg: an argument for example "add 5" is a simple
                  transform with arg = 5
    Methodes:
        self.do(obj): do transform on obj and return resulting new obj
        self.undo(obj): undo this transform
        self.reverse(): return a new simple transform that is inverse of self

    """

    def __init__(self, arg):
        self.arg = arg

    def do(self, obj):
        pass

    def undo(self, obj):
        pass

    def inverse(self):
        pass

    def __repr__(self):
        return "<Simple Transform Base Class>"


class StAdd(SimpleTransform):
    def do(self, obj):
        return obj + self.arg

    def undo(self, obj):
        return obj - self.arg

    def inverse(self):
        return StAdd(-self.arg)

    def __repr__(self):
        return "<ST Add {}>".format(self.arg)


class StMul(SimpleTransform):
    def do(self, obj):
        return obj * self.arg

    def undo(self, obj):
        if self.arg == 0:
            return "Undefined"
        return obj / self.arg

    def inverse(self):
        if self.arg == 0:
            return "Undefined"
        return StMul(1 / self.arg)

    def __repr__(self):
        return "<ST Multiply by {}>".format(self.arg)


class StPow(SimpleTransform):
    def do(self, obj):
        return obj ** self.arg

    def undo(self, obj):
        if self.arg == 0:
            return "Undefined"
        return obj ** 1 / self.arg

    def inverse(self):
        if self.arg == 0:
            return "Undefined"
        return StPow(1 / self.arg)

    def __repr__(self):
        return "<ST Raise to {}>".format(self.arg)


class StSq(StPow):
    def __init__(self):
        super(self).__init__(2)


class StSqrt(StPow):
    def __init__(self):
        super(self).__init__(1 / 2)


class StCb(StPow):
    def __init__(self):
        super(self).__init__(3)


class StCbrt(StPow):
    def __init__(self):
        super(self).__init__(1 / 3)


class ComplexTransform:
    """ A list of successive simple transforms.
    You can achieve transforms like 2*x + 1
    Attributes:
        self.transforms: a list of simple transforms done in order
    Methodes:
        self.do(obj): take an obj and return a new obj after
                      applying transformation
        self.undo(obj): undo transform and return a new obj
        self.inverse(): return a transform that is inverse of self
    """

    def __init__(self, *simple_transforms):
        self.transforms = list(simple_transforms)

    def do(self, obj):
        for t in self.transforms:
            obj = t.do(obj)
        return obj

    def undo(self, obj):
        for t in self.transforms.__reversed__():
            obj = t.undo(obj)
        return obj

    def inverse(self):
        return ComplexTransform(*(t.inverse()
                                  for t in self.transforms.__reversed__()))


def test():
    add10 = StAdd(10)
    times2 = StMul(2)
    times2plus10 = ComplexTransform(times2, add10)

    x = 4
    new_x = times2plus10.do(x)
    assert times2plus10.undo(new_x) == x

    minus10over2 = times2plus10.inverse()
    assert minus10over2.do(new_x) == x


if __name__ == '__main__':
    test()
