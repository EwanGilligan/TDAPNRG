import os
import sys
import time

import numpy as np
import matplotlib

from src.randology import *
from src.pnrg import *

seed1 = 0xDEADBEEF
seed2 = 0xD978757273

rng = FromBinaryFile("../../random-org-seq/TrueRandom1", 12000)
# rng2 = FromBinaryFile("../../random-org-seq/TrueRandom2", 12000)
# fileRand = FromBinaryFile("../../pseudo-random-sequences/outXorShift32", 12000)
# python_rand = pythonRandom("Python Random")
# gameRand = GameRand(0xDEADBEEF)
# randu = Randu(0xDEADBEEF)
# lsfr = LFSR(0xDEADBEEF)
# glibc48 = Glibc(0x2197B942509FF4DB)
# quasirandom = Quasirandom()

generators = [Randu(seed1),
              Randu(seed2),
              Minstd(seed1),
              Minstd(seed2),
              Glibc(seed1),
              Glibc(seed2),
              pythonRandom(seed1),
              pythonRandom(seed2),
              EICG1(seed1),
              EICG1(seed2),
              LFSR(seed1),
              LFSR(seed2),
              FromBinaryFile("../../random-org-seq/TrueRandom2", 12000),
              FromBinaryFile("../../random-org-seq/TrueRandom3", 12000),
              Quasirandom(),
              GameRand(seed1),
              GameRand(seed2),
              ]
test = HypercubeTest(runs=10, number_of_points=12000, dimension=3, homology_dimension=0, filtration_size=40,
                     reference_rng=rng, scale=1)
test2 = HypercubeTest(runs=10, number_of_points=12000, dimension=3, homology_dimension=0, filtration_size=40,
                      reference_rng=rng, scale=0.45)
test3 = HypercubeTest(runs=10, number_of_points=12000, dimension=3, homology_dimension=0, filtration_size=40,
                      reference_rng=rng, scale=0.15)
test4 = HypercubeTest(runs=5, number_of_points=12000, dimension=3, homology_dimension=0, filtration_size=40,
                      reference_rng=rng, scale=0.075)
print("Scale:1.0")
test.test_generator_list(generators)
print("Scale:0.45")
test2.test_generator_list(generators)
print("Scale:0.15")
test3.test_generator_list(generators)
# print("Scale 0.075")
# test4.test_generator_list(generators)
