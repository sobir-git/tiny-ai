from __future__ import division, print_function

from itertools import chain
from seq_repr import *
from seq_logging import LogTree
from helper import match_seq

# loading well-known sequences
from database import known_sequences, WellKnownSequence
database = known_sequences


logformat = "{s} --> {n} \t{c}"
report = True
local_known_sequences = []


class SearchResult:
    """ Search result class
    Attributes:
        value: (number) the predicted value
        depth: (number) roughly number of "steps" of solution
        log_tree: (LogTree) object that contain the way to reach the result
        extra_info: (dict) containing some extra info
    """

    def __init__(self, value, depth=0, method=None,
                 extra_info=None, log_tree=LogTree()):
        self.value = value
        self.depth = depth
        self.extra_info = extra_info
        self.log_tree = log_tree

    def __repr__(self):
        return "<SearchResult value={}, depth={}>".format(self.value,
                                                          self.depth)


def byLookUp(seq, depth_limit):
    # predict by matching to sequences in database (known_sequences)

    match_size, next_number, matching_seq = 0, None, None
    for s in chain(local_known_sequences, database):
        size, number = match_seq(seq, s)
        if size > match_size:
            next_number = number
            match_size = size
            matching_seq = s

    if not matching_seq or match_size < matching_seq.familiarity:
        return SearchResult(None)

    # create log tree
    c = "match with {}".format(matching_seq.readable()[:15], match_size)
    log = logformat.format(s=seq.readable(), n=next_number, c=c)
    log_tree = LogTree()
    log_tree.add_child(log)

    extra_info = {"matching sequence": matching_seq}
    return SearchResult(value=next_number,
                        depth=1,
                        log_tree=log_tree,
                        extra_info=extra_info)


def byAlter(seq, depth_limit):
    # predict by looking numbers in even and odd positions seperately
    ar = AlterRepr.convert(seq)

    result_evens = recursiveFindNext(ar.evens, min(depth_limit / 2, 2))
    next_even, depth1 = result_evens.value, result_evens.depth
    if next_even is None:
        return SearchResult(None)

    result_odds = recursiveFindNext(ar.odds, min(depth_limit / 2, 2))
    next_odd, depth2 = result_odds.value, result_odds.depth
    if next_odd is None:
        return SearchResult(None)

    # create log tree
    log_tree = LogTree()

    log = logformat.format(s=ar.evens.readable(),
                           n=next_even,
                           c="even positions")
    log_tree.add_child(log)
    log_tree.add_child(result_evens.log_tree)

    log = logformat.format(s=ar.odds.readable(), n=next_odd, c="odd position")
    log_tree.add_child(log)
    log_tree.add_child(result_odds.log_tree)

    # appending new predicted number
    if len(ar.evens) == len(ar.odds):
        ar.evens.append(next_even)
    else:
        ar.odds.append(next_odd)

    value = ar.toNormal()[-1]
    depth = max(depth1, depth2)
    result = SearchResult(value=value,
                          depth=depth + 1,
                          log_tree=log_tree)
    return result


def byDivMod(seq, depth_limit):
    # predict by looking at divs and mods (of sucessive terms) seperately
    if not DivModRepr.isConsidering(seq):
        return SearchResult(None)

    dm = DivModRepr(seq)

    result_divs = recursiveFindNext(dm.divs, min(depth_limit / 2, 2))
    next_div, depth1 = result_divs.value, result_divs.depth
    if next_div is None:
        return SearchResult(None)

    result_mods = recursiveFindNext(dm.mods, min(depth_limit / 2, 2))
    next_mod, depth2 = result_mods.value, result_mods.depth
    if next_mod is None:
        return SearchResult(None)

    # create log tree
    log_tree = LogTree()

    log = logformat.format(s=dm.divs.readable(), n=next_div, c="taking divs")
    log_tree.add_child(log)
    log_tree.add_child(result_divs.log_tree)

    log = logformat.format(s=dm.mods.readable(), n=next_mod, c="taking mods")
    log_tree.add_child(log)
    log_tree.add_child(result_mods.log_tree)

    # appending new numbers
    dm.divs.append(next_div)
    dm.mods.append(next_mod)
    value = dm.toNormal()[-1]
    depth = max(depth1, depth2)
    return SearchResult(value=value,
                        depth=1 + depth,
                        log_tree=log_tree)


def byDivMod2(seq, depth_limit):
    """Predict by looking at divs2 and mods2 (of sucessive terms)
    seperately """
    if not DivModRepr2.isConsidering(seq):
        return SearchResult(None)

    dm = DivModRepr2(seq)

    result_divs = recursiveFindNext(dm.divs, min(depth_limit / 2, 2))
    next_div, depth1 = result_divs.value, result_divs.depth
    if next_div is None:
        return SearchResult(None)

    result_mods = recursiveFindNext(dm.mods, min(depth_limit / 2, 2))
    next_mod, depth2 = result_mods.value, result_mods.depth
    if next_mod is None:
        return SearchResult(None)

    # creating log tree
    log_tree = LogTree()

    log = logformat.format(s=dm.divs.readable(), n=next_div, c="taking divs")
    log_tree.add_child(log)
    log_tree.add_child(result_divs.log_tree)

    log = logformat.format(s=dm.mods.readable(), n=next_mod, c="taking mods")
    log_tree.add_child(log)
    log_tree.add_child(result_mods.log_tree)

    # appending new numbers
    dm.divs.append(next_div)
    dm.mods.append(next_mod)
    value = dm.toNormal()[-1]
    depth = max(depth1, depth2)
    return SearchResult(value=value,
                        depth=1 + depth,
                        log_tree=log_tree)


def byDiff(seq, depth_limit):
    """ predict by considering differences """
    d = DiffRepr.convert(seq)
    result = recursiveFindNext(d.differences, depth_limit)
    next_difference, depth = result.value, result.depth

    if next_difference is None:
        return SearchResult(None)

    # creating log tree
    log = logformat.format(s=d.differences.readable(),
                           n=next_difference,
                           c="taking differences")
    log_tree = LogTree()
    log_tree.add_child(log)
    log_tree.add_child(result.log_tree)

    # appending new numbers
    d.differences.append(next_difference)

    return SearchResult(value=d.toNormal()[-1],
                        depth=depth + 1,
                        log_tree=log_tree)


def byRatio(seq, depth_limit):
    """ predict by considering ratios of sucessive terms"""
    if not RatioRepr.isConsidering(seq):
        return SearchResult(None)

    rr = RatioRepr.convert(seq)
    result = recursiveFindNext(rr.ratios, depth_limit)
    next_ratio, depth = result.value, result.depth
    if next_ratio is None:
        return SearchResult(None)

    # create log_tree
    log_tree = LogTree()
    log = logformat.format(s=rr.ratios.readable(),
                           n=next_ratio,
                           c="taking ratios")
    log_tree.add_child(log)
    log_tree.add_child(result.log_tree)

    # appending new numbers
    rr.ratios.append(next_ratio)
    return SearchResult(value=rr.toNormal()[-1],
                        depth=depth + 1,
                        log_tree=log_tree)


def byAbs(seq, depth_limit):
    """Predict by considering absolute values and signs seperately."""

    # if all numbers are positive then abort this search
    # (because it causes infinite recursion)
    if not AbsRepr.isConsidering(seq):
        return SearchResult(None)  # pretend to fail

    abs_seq = AbsRepr.convert(seq)

    result_values = recursiveFindNext(abs_seq.values, depth_limit)
    if result_values.value is None:
        return SearchResult(None)

    result_signs = recursiveFindNext(abs_seq.signs, min(depth_limit / 2, 2))
    if result_signs.value is None:
        return SearchResult(None)

    # create log tree
    log_tree = LogTree()

    log = logformat.format(s=abs_seq.values.readable(),
                           n=result_values.value,
                           c="taking absolute values")

    log_tree.add_child(log)
    log_tree.add_child(result_values.log_tree)

    log = logformat.format(s=abs_seq.signs.readable(),
                           n=result_signs.value,
                           c="taking signs")
    log_tree.add_child(log)
    log_tree.add_child(result_signs.log_tree)

    next_number = result_signs.value * result_values.value
    depth = 1 + max(result_values.depth, result_signs.depth)
    return SearchResult(value=next_number,
                        depth=depth,
                        log_tree=log_tree)


# all search functions
search_methodes = (byLookUp,
                   byDiff,
                   byRatio,
                   byDivMod,
                   byAlter,
                   byAbs,
                   byDivMod2)


def recursiveFindNext(seq, depth_limit):
    # cut off when reached depth limit
    if depth_limit <= 0:
        return SearchResult(None)

    # if sequence is too short
    if len(seq) < 2:
        return SearchResult(None)

    # if sequence is constant
    if seq.is_constant():
        return SearchResult(value=seq[0])

    answers = []  # a list of (possible_next_number, depth)
    for f in search_methodes:
        result = f(seq, depth_limit=depth_limit - 1)
        if result.value is not None:
            result.depth += 1
            answers.append(result)

            # can be sometimes helpful
            # if result.depth <= depth_limit:
            #     break

    # choose a result with minimum depth
    if not answers:
        return SearchResult(None)

    result = min(answers, key=lambda result: result.depth)
    return result


depth_limit = 70


def findNext(seq):
    # convert to normal
    seq = WellKnownSequence(seq, familiarity=3)
    local_known_sequences.append(seq)

    # getting result
    result = recursiveFindNext(seq, depth_limit)
    next_number = result.value

    # logging
    log_tree = LogTree()
    log = logformat.format(s=seq.readable(), n=next_number, c="")
    log_tree.add_child(log)
    log_tree.add_child(result.log_tree)

    # return next number
    return SearchResult(value=next_number, log_tree=log_tree)
