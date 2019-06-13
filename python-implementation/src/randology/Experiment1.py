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

rng = FromBinaryFile("TrueRandom1", 12000)
python_rand = pythonRandom("Python Random")
gameRand = GameRand(0xDEADBEEF)
randu = Randu(int(time.time()))
test = HypercubeTest(runs=10, number_of_points=12000, dimension=3, homology_dimension=0, filtration_size=20,
                     reference_rng=rng, max_filtration_value=0.1)
start = time.time()
print(test.perform_test(gameRand))
end = time.time()
print("Time elapsed:", end - start)
