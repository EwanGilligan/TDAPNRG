from randology.pnrg.CSG import QCG


class QCG631(QCG):
    def __init__(self, seed):
        super().__init__(a=6, b=3, increment=1, modulus=2 ** 32 - 1, seed=seed)
