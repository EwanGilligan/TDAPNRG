import numpy as np

from pnrg import RNG


class Xorshift128p(RNG):

    def __init__(self, seed1, seed2):
        super().__init__('Xorshift128+')
        self.a = np.int64(seed1)
        self.b = np.int64(seed2)

    def next_int(self) -> np.int64:
        t = self.a
        s = self.b
        self.a = s
        t ^= t << 23
        t ^= t >> 17
        t ^= (s >> 26)
        self.b = t
        return t + s

    def next_float(self) -> np.float64:
        return abs(self.next_int()) / np.iinfo(np.int64).max

    def next_64_bits(self) -> np.int64:
        return self.next_int()
