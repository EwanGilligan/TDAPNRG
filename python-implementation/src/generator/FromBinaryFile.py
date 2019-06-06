from src.generator.RNG import RNG


class FromBinaryFile(RNG):
    def __init__(self, filepath: str, size: int):
        RNG.__init__(self, "File-" + filepath.replace('/', '-'))
        try:
            self.f = open(filepath, "rb", size * 64)
        except IOError:
            print("Couldn't open file:", filepath)
            exit(1)

    def next_long(self):
        b0 = 0xFF & int.from_bytes(self.f.read(1), byteorder="little", signed=False)
        b1 = 0xFF & int.from_bytes(self.f.read(1), byteorder="little", signed=False)
        b2 = 0xFF & int.from_bytes(self.f.read(1), byteorder="little", signed=False)
        b3 = 0xFF & int.from_bytes(self.f.read(1), byteorder="little", signed=False)
        b4 = 0xFF & int.from_bytes(self.f.read(1), byteorder="little", signed=False)
        b5 = 0xFF & int.from_bytes(self.f.read(1), byteorder="little", signed=False)
        b6 = 0xFF & int.from_bytes(self.f.read(1), byteorder="little", signed=False)
        b7 = 0xFF & int.from_bytes(self.f.read(1), byteorder="little", signed=False)
        return b7 | (b6 << 8) | (b5 << 16) | (b4 << 24) | (b3 << 32) | (b2 << 40) | (b1 << 48) | (b0 << 56)

    def next_double(self):
        return abs(self.next_long() / (2 ** 63 - 1))

    def next_64_bits(self):
        return self.next_long()
