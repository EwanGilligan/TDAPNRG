from .LCG import LCG


class Minstd(LCG):

    def __init__(self, seed):
        super().__init__("Minstd", 16807, 0, 2147483647, seed)
