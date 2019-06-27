import numpy as np

from src.pnrg import RNG


def lrshift(val, n) -> np.int64:
    """
    Logically right shifts value by n places.
    :param val: value to shift
    :param n: number of bits to shift by.
    :return: result of right shift.
    """
    return (val % (1 << 64)) >> n


class LFSR(RNG):

    def __init__(self, seed: np.int64):
        super().__init__("LFSR2547")
        self.register = np.int64(seed)

    def rotate1(self):
        b25 = lrshift(self.register, 25) & 1
        b47 = lrshift(self.register, 47) & 1
        bit = b25 ^ b47
        self.register = (self.register << 1) | bit

    def rotate(self):
        for i in range(64):
            self.rotate1()

    def next_int(self) -> np.int64:
        self.rotate()
        return self.register

    def next_float(self) -> np.float64:
        return abs(self.next_int() / np.iinfo(np.int64).max)

    def next_64_bits(self) -> np.int64:
        return self.next_int()
