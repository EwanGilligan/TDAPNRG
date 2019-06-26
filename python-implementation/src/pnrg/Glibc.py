from src.pnrg import LCG


class Glibc(LCG):

    def __init__(self, seed):
        super().__init__("Glibc48", 25214903917, 11, 2 ** 48, seed)
