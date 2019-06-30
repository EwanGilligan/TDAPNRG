from src.pnrg import FromBinaryFile, Randu
from src.randology import MatrixRankTest

rng = FromBinaryFile("../random-org-seq/TrueRandom1", 12000)
randu = Randu(1)
for i in range(10):
    m = MatrixRankTest.create_random_matrix(rng, 4)
    print(MatrixRankTest.rank(m))

