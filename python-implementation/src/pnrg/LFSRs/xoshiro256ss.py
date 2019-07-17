import numpy as np

from pnrg import RNG


class Xoshiro256ss(RNG):
    """
    Adapted from http://xoshiro.di.unimi.it/
    """
    # maximum value when calculating floating point values, as only the upper 53 bits are used.
    max_float = (1 << 53 - 1)

    def __init__(self, state: np.ndarray):
        super().__init__('Xoshiro256**')
        assert state.shape == (4,), "State should only have 4 values."
        self.state = state.astype(np.uint64)

    def next_uint(self) -> np.int64:
        result = Xoshiro256ss.rol64(self.state[1] * 5, 7) * 9

        t = self.state[1] << 17

        self.state[2] ^= self.state[0]
        self.state[3] ^= self.state[1]
        self.state[1] ^= self.state[2]
        self.state[0] ^= self.state[3]

        self.state[2] ^= t

        self.state[3] = Xoshiro256ss.rol64(self.state[3], 45)
        return result

    def next_int(self) -> np.int64:
        return np.int64(self.next_uint())

    def next_float(self) -> np.float64:
        # Only take the upper 53 bits for floating points.
        return np.int64(self.next_uint() >> 11) / Xoshiro256ss.max_float

    def next_64_bits(self) -> np.int64:
        return self.next_int()

    @staticmethod
    def rol64(x: np.int64, k: int) -> np.uint64:
        return (x << k) | (x >> (64 - k))
