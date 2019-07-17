import numpy as np

from pnrg import RNG
from hashlib import sha256


class SHA(RNG):

    def __init__(self, hashobj, seed: np.int64):
        super().__init__(hashobj.__name__)
        self.hash = hashobj
        self.seed = np.int64(seed)

    def next_int(self) -> np.int64:
        self.seed += 1
        hashed_bytes = self.hash(bytes(self.seed))
        int_value = int.from_bytes(hashed_bytes.digest(), byteorder='little') % np.iinfo(np.int64).max
        return np.int64(int_value)

    def next_float(self) -> np.float64:
        return self.next_int() / np.iinfo(np.int64).max

    def next_64_bits(self) -> np.int64:
        return self.next_int()
