import numpy as np

from src.pnrg import RNG


class ICG(RNG):

    def __init__(self, multiplier, increment, modulus, seed, name=None):
        if name is None:
            name = "ICG-" + str(multiplier) + "-" + str(increment) + "-" + str(modulus)
        super().__init__(name)
        self.multiplier = np.int64(multiplier)
        self.increment = np.int64(increment)
        self.modulus = np.int64(modulus)
        self.seed = np.int64(seed)

    def next_int(self) -> np.int64:
        seed = self.inverse_mod(self.seed * self.multiplier + self.increment, self.modulus)
        return seed

    def next_float(self) -> np.float64:
        return abs(self.next_int() / self.modulus)

    def next_64_bits(self) -> np.int64:
        high = self.next_int()
        med = self.next_int()
        low = self.next_int()
        result = (high << 33) ^ (med << 2) ^ (low << 62 >> 62)
        return result

    @staticmethod
    def inverse_mod(a: np.int64, b: np.int64):
        b0 = b
        t = 0
        q = 0
        x0 = 0
        x1 = 1
        if b == 1:
            return 1
        while a > 1 and b > 0:
            q = a / b
            t = b
            b = a % b
            a = t
            t = x0
            x0 = x1 - q * x0
            x1 = t
        if x1 < 0:
            x1 += b0
        return np.int64(x1)
