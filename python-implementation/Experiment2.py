from src.pnrg import FromBinaryFile, Randu
from src.randology import MatrixRankTest

rng = FromBinaryFile("../random-org-seq/TrueRandom1", 12000)
randu = Randu(1)
test = MatrixRankTest(rng, runs=1, number_of_points=100, matrix_size=64, homology_dimension=0)
test.test_generator_list([randu])

