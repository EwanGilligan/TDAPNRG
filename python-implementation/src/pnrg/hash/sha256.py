from pnrg.hash.sha import SHA
from hashlib import sha256


class SHA256(SHA):
    def __init__(self, seed, salt):
        super().__init__(sha256, seed, salt)
