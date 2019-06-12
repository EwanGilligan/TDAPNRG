import os
import sys
import time

import numpy as np
import matplotlib

from src.generator.FromBinaryFile import FromBinaryFile
from src.generator.Randu import Randu
from src.randology.HypercubeTest import HypercubeTest
rng = FromBinaryFile("TrueRandom1", 12000)

randu = Randu(int(time.time()))
test = HypercubeTest(runs=5, number_of_points=12000, dimension=3, max_simplex_dim=1, filtration_size=50, reference_rng=rng)
print(test.perform_test(rng))


