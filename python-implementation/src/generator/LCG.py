from src.generator.RNG import RNG


class LCG(RNG):

    def __init__(self, name: str, multiplier: int, increment: int, modulus: int, seed: int) -> None:
        RNG.__init__(self, name)
        self.multiplier = multiplier
        self.increment = increment
        self.modulus = modulus
        self.seed = seed

    def next_long(self):
        self.seed = (self.seed * self.multiplier + self.increment) % self.modulus
        return self.seed

    def next_double(self):
        return abs(self.next_long() / self.modulus)

    def next_64_bits(self):
        high = self.next_long()
        med = self.next_long()
        low = self.next_long()
        return (high << 33) ^ (med << 2) ^ (low << 62 >> 62)
