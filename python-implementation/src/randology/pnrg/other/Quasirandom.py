import numpy as np

from randology.pnrg import RNG


class Quasirandom(RNG):
    C0 = 4.7596266423396880
    C1 = 5.3205298191322060
    C2 = 2.2419207148157443
    M0 = 0.9060939428196817
    M1 = 0.5393446629166316
    M2 = 1.0471975511965976

    def __init__(self):
        super().__init__("Quasirandom")
        self.seed = 0

    def next_int(self) -> np.int64:
        return round(self.next_float() * np.iinfo(np.int64).max)

    def next_float(self) -> np.float64:
        self.seed += 1
        x = self.seed
        rem = x % 3
        if rem == 0:
            return (Quasirandom.C0 + x * Quasirandom.M0) % 1
        elif rem == 1:
            return (Quasirandom.C1 + x * Quasirandom.M1) % 1
        elif rem == 2:
            return (Quasirandom.C2 + x * Quasirandom.M2) % 1

    def next_64_bits(self) -> np.int64:
        return self.next_int()
