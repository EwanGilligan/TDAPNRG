import os
import sys

import numpy as np
import matplotlib

from src.generator.FromBinaryFile import FromBinaryFile
from src.generator.Randu import Randu
from src.randology.HypercubeTest import HypercubeTest
rng = FromBinaryFile("TrueRandom1", 40)
randu = Randu(1390808)
#test = HypercubeTest(runs=30, number_of_points=100, dimension=3, max_simplex_dim=1)
#test.single_run(randu, None)
print(sys.getsizeof(np.int64(4)))

