from pnrg.CSG.QCG import QCG


class QCG981(QCG):
    def __init__(self, seed):
        super().__init__(a=10, b=5, increment=1, modulus=2 ** 32 - 1, seed=seed)
