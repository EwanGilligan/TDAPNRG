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


# rng = FromBinaryFile("TrueRandom2", 12000)
# rng2 = FromBinaryFile("TrueRandom2", 12000)
# python_rand = pythonRandom("Python Random")
# gameRand = GameRand(0xDEADBEEF)
# randu = Randu(int(time.time()))
# test = HypercubeTest(runs=1, number_of_points=24000, dimension=3, homology_dimension=0, filtration_size=20,
# reference_rng = rng)
# test.visualise_failure(randu)
# start = time.time()
# print(test.perform_test(randu))
# end = time.time()
# print("Time elapsed:", end - start)


def test_directory(directory_path):
    rng = FromBinaryFile("src/randology/TrueRandom2", 12000)
    test = HypercubeTest(runs=10, number_of_points=12000, dimension=3, homology_dimension=0, filtration_size=20,
                         reference_rng=rng, max_filtration_value=0.1)
    for filename in os.listdir(directory_path):
        test_rng = FromBinaryFile(directory_path + '/' + filename, 12000)
        start = time.time()
        passes = test.perform_test(test_rng)
        end = time.time()
        print('{}:{}/{}'.format(test_rng.get_name(), passes, test.runs))
        print("Time elapsed:", end - start)
    print("Done")


test_directory("../pseudo-random-sequences")
