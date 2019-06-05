from src.generator.LCG import LCG


class Randu(LCG):
    def __init__(self, seed):
        LCG.__init__(self, "Randu", 65539, 0, 2 ** 31, seed)


randu = Randu(1)
for i in range(0, 10):
    print(randu.next_long())
