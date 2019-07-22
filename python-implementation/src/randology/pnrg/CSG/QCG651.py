from randology.pnrg.CSG import QCG


class QCG651(QCG):
    def __init__(self, seed):
        super().__init__(a=6, b=5, increment=1, modulus=2 ** 32 - 1, seed=seed)
