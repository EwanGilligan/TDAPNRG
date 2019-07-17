import numpy as np

from pnrg import RNG

np.seterr(over='ignore')

class Xoshiro256ss(RNG):
    """
    Adapted from http://xoshiro.di.unimi.it/
    """
    # maximum value when calculating floating point values, as only the upper 53 bits are used.
    max_float = (1 << 53)
    # casted constants.
    u_5 = np.uint64(5)
    u_7 = np.uint64(7)
    u_9 = np.uint64(9)
    u_11 = np.uint64(11)

    def __init__(self, state: np.ndarray):
        super().__init__('Xoshiro256**')
        assert state.shape == (4,), "State should only have 4 values."
        self.state = state.astype(np.uint64)

    def next_uint(self) -> np.int64:
        result = Xoshiro256ss.rol64(self.state[1] * self.u_5, self.u_7) * self.u_9

        t = self.state[1] << np.uint64(17)

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
        return (self.next_uint() >> self.u_11) / Xoshiro256ss.max_float

    def next_64_bits(self) -> np.int64:
        return self.next_int()

    @staticmethod
    def rol64(x: np.uint64, k) -> np.uint64:
        return (x << np.uint64(k)) | (x >> np.uint64(64 - k))

