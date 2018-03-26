from seq_repr import NormalRepr


class WellKnownSequence(NormalRepr):
    """ Well known sequences
    Attributes:
        familiarity: size of smallest part that isneeded to recognize
                     the sequence
    """

    def __init__(self, *args, familiarity=3, **kwargs):
        super().__init__(*args, **kwargs)
        self.familiarity = familiarity


known_sequences = [
    WellKnownSequence([i**2 for i in range(1, 12)], familiarity=3),
    WellKnownSequence([i**3 for i in range(1, 7)], familiarity=3),
    WellKnownSequence([2**i for i in range(0, 12)], familiarity=3),
    WellKnownSequence([3**i for i in range(0, 8)], familiarity=3),
    WellKnownSequence([4**i for i in range(0, 7)], familiarity=3),
    WellKnownSequence([10**i for i in range(0, 5)], familiarity=3),
    WellKnownSequence([2, 3, 5, 7, 11, 13, 17, 19, 23], familiarity=4),
]

reverses = [s.reversed_copy() for s in known_sequences]
known_sequences.extend(reverses)
