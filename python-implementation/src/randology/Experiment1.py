import os
import sys
import time

import numpy as np
import matplotlib

from src.generator.FromBinaryFile import FromBinaryFile
from src.generator.Randu import Randu
from src.generator.pythonRandom import pythonRandom
from src.randology.HypercubeTest import HypercubeTest
rng = FromBinaryFile("TrueRandom1", 12000)
python_rand = pythonRandom("Python Random")

randu = Randu(int(time.time()))
test = HypercubeTest(runs=10, number_of_points=12000, dimension=3, max_simplex_dim=0, filtration_size=50, reference_rng=rng)
print(test.perform_test(randu))
print(test.perform_test(python_rand))


