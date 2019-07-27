import numpy as np

from randology.pnrg import RNG


class QCG(RNG):
    def __init__(self, a, b, increment, modulus, seed):
        super().__init__("QCG{}{}{}-{}".format(a, b, increment, modulus))
        self.a = np.int64(a)
        self.b = np.int64(b)
        self.increment = np.int64(increment)
        self.modulus = np.int64(modulus)
        self.seed = np.int64(seed) % modulus

    def next_int(self) -> np.int64:
        self.seed = (self.seed * self.seed * self.a + self.seed * self.b + self.increment) % self.modulus
        return self.seed

    def next_float(self) -> np.float64:
        return abs(self.next_int() / self.modulus)

    def next_64_bits(self) -> np.int64:
        high = self.next_int()
        med = self.next_int()
        low = self.next_int()
        result = (high << 33) ^ (med << 2) ^ (low << 62 >> 62)
        return result
