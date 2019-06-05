from src.generator.RNG import RNG


class FromBinaryFile(RNG):
    def __init__(self, filepath: str, size: int):
        RNG.__init__(self, "File-" + filepath.replace('/', '-'))
        try:
            self.f = open(filepath, "rb", size * 64)
        except IOError:
            exit(1)

    def next_long(self):
        b0 = 0xFF & int(self.f.read(1))
        b1 = 0xFF & int(self.f.read(1))
        b2 = 0xFF & int(self.f.read(1))
        b3 = 0xFF & int(self.f.read(1))
        b4 = 0xFF & int(self.f.read(1))
        b5 = 0xFF & int(self.f.read(1))
        b6 = 0xFF & int(self.f.read(1))
        b7 = 0xFF & int(self.f.read(1))
        return b7 | (b6 << 8) | (b5 << 16) | (b4 << 24) | (b3 << 32) | (b2 << 40) | (b1 << 48) | (b0 << 56)

    def next_double(self):
        return abs(self.next_long() / 2**64)

    def next_64_bits(self):
        return self.next_long()
