import numpy as np

from randology.pnrg import RNG


def lrshift(val, n) -> np.int64:
    """
    Logically right shifts value by n places.
    :param val: value to shift
    :param n: number of bits to shift by.
    :return: result of right shift.
    """
    return (val % (1 << 64)) >> n


class XorShift32(RNG):

    def __init__(self, seed):
        super().__init__("XorShift32")
        self.state = np.int32(seed)

    def next_32_int(self):
        self.state ^= (self.state << 13)
        self.state ^= lrshift(self.state, 17)
        self.state ^= (self.state << 5)
        return self.state

    def next_int(self) -> np.int64:
        a = np.int64(self.next_32_int())
        b = np.int64(self.next_32_int())
        return (a << 32) ^ b

    def next_float(self) -> np.float64:
        return abs(self.next_int()) / np.iinfo(np.int64).max

    def next_64_bits(self) -> np.int64:
        return self.next_int()
