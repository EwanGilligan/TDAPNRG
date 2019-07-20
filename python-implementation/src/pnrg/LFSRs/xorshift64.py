import numpy as np

from pnrg import RNG


def lrshift(val, n) -> np.int64:
    """
    Logically right shifts value by n places.
    :param val: value to shift
    :param n: number of bits to shift by.
    :return: result of right shift.
    """
    return (val % (1 << 64)) >> n


class XorShift64(RNG):

    def __init__(self, seed):
        super().__init__("XorShift64")
        self.state = np.int64(seed)

    def next_int(self) -> np.int64:
        self.state ^= (self.state << 21)
        self.state ^= lrshift(self.state, 35)
        self.state ^= (self.state << 4)
        return self.state

    def next_float(self) -> np.float64:
        return abs(self.next_int()) / np.iinfo(np.int64).max

    def next_64_bits(self) -> np.int64:
        return self.next_int()
