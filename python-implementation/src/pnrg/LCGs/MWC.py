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

class MWC(RNG):
    """
    An implementation of the Multiply-With-Carry generator from Numerical Recipes
    """
    def __init__(self, seed):
        super().__init__("MWCNR")
        self.seed = np.int64(seed)
        self.multiplier = np.int64(0xffffda61)

    def next_32_int(self) -> np.int32:
        self.seed = self.multiplier * (np.int32(self.seed) + lrshift(self.seed, 32))
        return np.int32(self.seed)

    def next_int(self) -> np.int64:
        left = np.int64(self.next_32_int())
        right = np.int64(self.next_32_int())
        return (left << 32) ^ right

    def next_float(self) -> np.float64:
        return abs(self.next_int() / np.iinfo(np.int64).max)

    def next_64_bits(self) -> np.int64:
        return self.next_int()