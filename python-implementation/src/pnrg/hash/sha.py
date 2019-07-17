import numpy as np

from pnrg import RNG
from hashlib import sha256, sha512, sha384, sha1


class SHA(RNG):

    def __init__(self, hash_obj, seed: np.int64, salt: str):
        """
        Initialisation of SHA generator.

        :param hash_obj: function to use to hash objects.
        :param seed: The seed of the generator.
        :param salt: salt for the hashing algorithm to use.
        """
        super().__init__(hash_obj.__name__)
        self.hash_obj = hash_obj
        self.seed = np.int64(seed)
        self.salt = salt.encode('utf-8')

    def next_int(self) -> np.int64:
        self.seed += 1
        hashed_bytes = self.hash_obj(bytes(self.seed))
        hashed_bytes.update(self.salt)
        int_value = int.from_bytes(hashed_bytes.digest(), byteorder='little') % np.iinfo(np.int64).max
        return np.int64(int_value)

    def next_float(self) -> np.float64:
        return self.next_int() / np.iinfo(np.int64).max

    def next_64_bits(self) -> np.int64:
        return self.next_int()


class SHA256(SHA):
    def __init__(self, seed, salt):
        super().__init__(sha256, seed, salt)


class SHA512(SHA):
    def __init__(self, seed, salt):
        super().__init__(sha512, seed, salt)


class SHA384(SHA):
    def __init__(self, seed, salt):
        super().__init__(sha384, seed, salt)


class SHA1(SHA):
    def __init__(self, seed, salt):
        super().__init__(sha1, seed, salt)
