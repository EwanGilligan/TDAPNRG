import os
import sys
import time

import numpy as np
import matplotlib

from src.randology import *
from src.pnrg import *

rng = FromBinaryFile("../random-org-seq/TrueRandom1", 12000)
rng2 = FromBinaryFile("../random-org-seq/TrueRandom2", 12000)
python_rand = pythonRandom("Python Random")
gameRand = GameRand(0xDEADBEEF)
randu = Randu(int(time.time()))
test = HypercubeTest(runs=2, number_of_points=12000, dimension=4, homology_dimension=0, filtration_size=20,
                     reference_rng=rng, scale=1.0)
# test.visualise_failure(randu)
start = time.time()
print(test.perform_test(rng2))
end = time.time()
print("Time elapsed:", end - start)


#test.test_directory("../pseudo-random-sequences")
