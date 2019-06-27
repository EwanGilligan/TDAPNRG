import numpy as np
import random

from src.pnrg.RNG import RNG


class pythonRandom(RNG):

    def __init__(self, seed=None):
        super().__init__("PythonRandom")
        if seed is not None:
            random.seed(seed)

    def next_int(self) -> np.int64:
        return np.int64(random.randint(0, 2 ** 63 - 1))

    def next_float(self) -> np.float64:
        return np.float64(random.random())

    def next_64_bits(self):
        return np.float64(random.getrandbits(64))
