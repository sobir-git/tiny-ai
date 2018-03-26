import search
from search import findNext

search.depth_limit = 7


def test():
    search.report = False
    assert findNext([1, 2, 3, 4]).value == 5
    assert findNext([1, 4, 9]).value == 16
    assert findNext([1, 8, 27]).value == 64
    assert findNext([23, 34, 45, 56, 67]).value == 78
    assert findNext([0, 1, 0, 1]).value == 0
    assert findNext([12, 15, 21, 24, 30]).value == 33
    assert findNext([1, 2, 4, 8]).value == 16
    assert findNext([1, 3, 9, 27]).value == 81
    assert findNext([2, 5, 14, 41]).value == 122
    assert findNext([1, -2, 3, -4]).value == 5
    assert findNext([1, -2, 4, -8, 16]).value == -32
    assert findNext([4, 6, 9, 13, 18]).value == 24
    assert findNext([12, 15, 21, 24, 30]).value == 33
    assert findNext([1, 1, 2, 3, 5, 8]).value == 13
    assert findNext([-2, 4, -12, 48, -240]).value == 1440
    assert findNext([1, 10, 3, 9, 5, 8, 7, 7]).value == 9
    assert findNext([2, 3, 5, 7, 11, 13, 17, 19]).value == 23
    assert findNext([200, 196, 180, 116]).value == -140
    assert findNext([144, 121, 100, 81]).value == 64
    assert findNext([3, 10, 20, 27, 37]).value == 44
    assert findNext([80, 10, 70, 15, 60]).value == 20
    assert findNext([8, 6, 9, 23, 87]).value == 429
    assert findNext([5, 11, 23, 47]).value == 95
    assert findNext([7, 13, 24, 45]).value == 86
    assert findNext([14, 28, 20, 40, 32, 64]).value == 56
    assert findNext([1, 1, 2, 3, 5]).value in {8, 7}
    # assert findNext() == 5              # --> 5
    # assert findNext() == 5              # --> 5


if __name__ == "__main__":
    from time import time
    # seq = [21, 24, 30, 33, 39, 51]    # --> 56 **
    # seq = [101, 112, 131, 415, 161, 718]  # --> 192 (10, 11, 12, 13, 14 ...) **
    # seq = [1, 2, 3, 4, 1, 2, 3, 4, 2, 1]  # related to roman numbers **
    # seq = [20000, 2000, 200, 20]  # --> 2 (ratio but reversed) **
    # seq = [243, 162, 108, 72]  # --> 49 (times 2/3) **
    # seq = [2, 5, 10, 50]  # --> 500
    # seq = [99, 1616, 2525, 3636]  # --> 4949
    # seq = [44, 99, 166, 255]  # --> 4949
    # seq = [1000, 100, 10]  # --> 1
    # seq = [1, 3, 5, 11, 21] # -->  43
    seq = [1, 6, 28, 145]             # --> 876 (times 2 + i) **
    seq = [4, 2, 3, 4, 6, 2, 3]
    start_time = time()
    # test()
    res = findNext(seq)
    print('\n'.join(res.log_tree.string()))
    print("Search finished in {}s".format(round(time() - start_time, 3)))
