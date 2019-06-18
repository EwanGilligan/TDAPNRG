import os
import sys
import time

import numpy as np
import matplotlib

from src.generator.FromBinaryFile import FromBinaryFile
from src.generator.GameRand import GameRand
from src.generator.Randu import Randu
from src.generator.pythonRandom import pythonRandom
from src.randology.HypercubeTest import HypercubeTest


rng = FromBinaryFile("TrueRandom2", 12000)
rng2 = FromBinaryFile("TrueRandom2", 12000)
python_rand = pythonRandom("Python Random")
gameRand = GameRand(0xDEADBEEF)
randu = Randu(int(time.time()))
test = HypercubeTest(runs=10, number_of_points=12000, dimension=3, homology_dimension=0, filtration_size=20,
reference_rng = rng)
#test.visualise_failure(randu)
start = time.time()
print(test.perform_test(rng2))
end = time.time()
print("Time elapsed:", end - start)




#test_directory("../pseudo-random-sequences")
