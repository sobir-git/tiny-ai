from helper import iter_pairs


class SequenceTransform:
    """ A base class for transforming sequences """

    def do(self, seq):
        return NotImplemented


# A transform for taking difference of sucessive terms in a sequence
difference = SequenceTransform()


def take_difference(seq):
    return [nxt - prv for nxt, prv in iter_pairs(seq)]


difference.do = take_difference


def test():
    s = [2, 3, 4, 5]
    assert difference.do(s) == [1, 1, 1]
