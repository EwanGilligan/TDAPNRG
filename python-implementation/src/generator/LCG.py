from src.generator.RNG import RNG
import numpy as np


class LCG(RNG):

    def __init__(self, name: str, multiplier: int, increment: int, modulus: int, seed: int) -> None:
        RNG.__init__(self, name)
        self.multiplier = multiplier
        self.increment = increment
        self.modulus = modulus
        self.seed = seed

    def next_int(self):
        self.seed = (self.seed * self.multiplier + self.increment) % self.modulus
        return self.seed

    def next_float(self):
        return abs(self.next_int() / self.modulus)

    def next_64_bits(self):
        high = self.next_int()
        med = self.next_int()
        low = self.next_int()
        return (high << 33) ^ (med << 2) ^ (low << 62 >> 62)
