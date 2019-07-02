from src.pnrg.RNG import RNG
import sys
import numpy as np


class FromBinaryFile(RNG):
    def __init__(self, filepath: str, size: int, name = None):
        if name is None:
            name = "File-" + filepath.replace('/', '-')
        RNG.__init__(self, name)
        try:
            self.f = open(filepath, "rb", size * 64)
        except IOError:
            print("Couldn't open file:", filepath)
            exit(1)

    def next_int(self):
        # b0 = 0xFF & int.from_bytes(self.f.read(1), byteorder="little", signed=False)
        # b1 = 0xFF & int.from_bytes(self.f.read(1), byteorder="little", signed=False)
        # b2 = 0xFF & int.from_bytes(self.f.read(1), byteorder="little", signed=False)
        # b3 = 0xFF & int.from_bytes(self.f.read(1), byteorder="little", signed=False)
        # b4 = 0xFF & int.from_bytes(self.f.read(1), byteorder="little", signed=False)
        # b5 = 0xFF & int.from_bytes(self.f.read(1), byteorder="little", signed=False)
        # b6 = 0xFF & int.from_bytes(self.f.read(1), byteorder="little", signed=False)
        # b7 = 0xFF & int.from_bytes(self.f.read(1), byteorder="little", signed=False)
        # return b7 | (b6 << 8) | (b5 << 16) | (b4 << 24) | (b3 << 32) | (b2 << 40) | (b1 << 48) | (b0 << 56)
        byte = self.f.read(8)
        # checks that the end of the file hasn't been reached.
        if not byte:
            # loops back to the beginning
            self.f.seek(0)
        return np.int64(int.from_bytes(byte, byteorder="little", signed=True))

    def next_float(self):
        return np.float64(abs(self.next_int() / (2**63 - 1)))

    def next_64_bits(self):
        return np.int64(self.next_int())
