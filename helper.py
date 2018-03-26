def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def write_primes(n):
    """Writes prime numbers to file "prime_numbers" as a list"""
    primes = [2, 3, 5, 7, 11]
    for i in range(primes[-1] + 1, n):
        for j in primes:
            if i % j == 0:
                break
        else:
            primes.append(i)

    with open("prime_numbers", 'w') as f:
        f.write(str(primes))


def read_primes():
    """Reads prime numbers from file "prime_numbers"
    and returns it as a list"""
    with open("prime_numbers", "r") as f:
        return eval(f.readline())


def iter_pairs(seq, cycle=False):
    """Iterates like (seq[i], seq[i+1])"""
    it = iter(seq)
    i = next(it)
    for j in it:
        yield (i, j)
        i = j

    if cycle:
        yield (i, seq[0])


def isConstant(seq):
    """ Check if seq is constant """
    first = seq[0]
    for i in seq:
        if i != first:
            return False
    return True


def match_seq(s, seq):
    """try to match the sequences s[i:] to seq[a:b] (b < len(s2))
    return a tuple: (the size of the longest match, seq[b])
    """

    # print(s, seq)

    match_size, match_b = 0, len(seq) - 1
    for b in range(len(seq) - 2, -1, -1):
        # print('b=', b)
        b_, j = b, len(s) - 1
        fail = False

        while b_ != -1 and j != -1:
            # print('b_=', b_)
            # print('j=', j)
            if seq[b_] != s[j]:
                fail = True
                break
            b_, j = b_ - 1, j - 1

        if not fail and match_size < b - b_:
            match_size = b - b_
            match_b = b

    if match_size < 3:
        return (0, None)

    return (match_size, seq[match_b + 1])


def test_match_seq():
    seq = [1, 4, 9, 16]
    s = [1, 4, 9]
    assert match_seq(s, seq) == (3, 16)

    seq = [1, 4, 9]
    s = [1, 4, 9]
    assert match_seq(s, seq) == (0, None)

    seq = [1, 2, 4, 8, 16, 32, 64, 128]
    s = [1, 2, 4]
    assert match_seq(s, seq) == (3, 8)

    seq = [1, 2, 4, 8, 16, 32, 64, 128]
    s = [2, 2, 4]
    assert match_seq(s, seq) == (0, None)


if __name__ == "__main__":
    # write_primes(100)
    # primes = read_primes()
    test_match_seq()
