import numpy as np

from pnrg import RNG


# This quadratic generator is from Webkit2, see https://gist.github.com/Protonk/5367430
class Webkit2(RNG):
    def __init__(self, seed):
        super().__init__("Webkit2")
        self.state = np.int64(seed)

    def next_int(self) -> np.int64:
        self.state += (self.state * self.state) ** 5
        return abs(self.state)

    def next_float(self) -> np.float64:
        return abs(self.next_int() / np.iinfo(np.int64).max)

    def next_64_bits(self) -> np.int64:
        return self.next_int()
