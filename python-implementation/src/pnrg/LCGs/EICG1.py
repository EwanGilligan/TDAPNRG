from pnrg.LCGs import EIG


class EICG1(EIG):

    def __init__(self, seed):
        super().__init__(16807, 1, 2147483647, seed, name="EICG1")
