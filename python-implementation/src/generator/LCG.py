from src.generator.RNG import RNG
import numpy as np


class LCG(RNG):

    def __init__(self, name: str, multiplier: np.int64, increment: np.int64, modulus: np.int64, seed: np.int64) -> None:
        RNG.__init__(self, name)
        self.multiplier = np.int64(multiplier)
        self.increment = np.int64(increment)
        self.modulus = np.int64(modulus)
        self.seed = np.int64(seed)

    def next_int(self) -> np.int64:
        self.seed = (self.seed * self.multiplier + self.increment) % self.modulus
        return self.seed

    def next_float(self) -> np.float64:
        return np.float64(abs(self.next_int() / self.modulus))

    def next_64_bits(self) -> np.int64:
        high = self.next_int()
        med = self.next_int()
        low = self.next_int()
        return np.int64((high << 33) ^ (med << 2) ^ (low << 62 >> 62))
