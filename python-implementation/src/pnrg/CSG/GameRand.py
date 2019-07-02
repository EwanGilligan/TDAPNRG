from src.pnrg.RNG import RNG
import numpy as np


class GameRand(RNG):
    def __init__(self, seed: int):
        super().__init__("GameRand")
        self.high = seed
        self.low = seed ^ 0xDEAFBABE49616E42

    def next_int(self):
        self.high = (self.high << 32) + (self.high >> 32)
        self.high = (self.high + self.low) % (2 ** 63 - 1)
        self.low = (self.low + self.high) % (2 ** 63 - 1)
        return self.high

    def next_float(self):
        return abs(self.next_int() / np.iinfo(np.int64).max)

    def next_64_bits(self):
        return self.next_int()
