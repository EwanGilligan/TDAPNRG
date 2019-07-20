import numpy as np

from pnrg import RNG


class BlumBlumShub(RNG):
    pq = np.int64(50159 * 50207)

    def __init__(self, seed):
        super().__init__("BlumBlumShub")
        self.state = np.int64(seed) % self.pq

    def next_int(self) -> np.int64:
        result = 0
        # to avoid as many lookups in the loop
        state = self.state
        for i in range(64):
            state = state * state % self.pq
            result = 2 * result + (state % 2)
        self.state = state
        return result

    def next_float(self) -> np.float64:
        return abs(self.next_int() / np.iinfo(np.int64).max)

    def next_64_bits(self) -> np.int64:
        return self.next_int()
