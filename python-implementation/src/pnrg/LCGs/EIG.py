from src.pnrg.LCGs.ICG import ICG
import numpy as np


class EIG(ICG):

    def __init__(self, multiplier, increment, modulus, seed, name=None):
        if name is None:
            name = "EIG-" + str(multiplier) + "-" + str(increment) + "-" + str(modulus)
        super().__init__(name=name, multiplier=multiplier, increment=increment, modulus=modulus, seed=seed)

    def next_int(self) -> np.int64:
        self.seed = (self.seed + 1) % self.modulus
        return super().inverse_mod((self.seed * self.multiplier + self.increment) % self.modulus, self.modulus)
