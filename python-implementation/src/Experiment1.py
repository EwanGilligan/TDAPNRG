import os
import sys
import time

import numpy as np
import matplotlib

from src.randology import *
from src.pnrg import *

seed1 = 0xDEADBEEF
seed2 = 0xD978757273

rng = FromBinaryFile("../random-org-seq/TrueRandom1", 12000)
# rng2 = FromBinaryFile("../random-org-seq/TrueRandom2", 12000)
# fileRand = FromBinaryFile("../pseudo-random-sequences/outXorShift32", 12000)
# python_rand = pythonRandom("Python Random")
# gameRand = GameRand(0xDEADBEEF)
# randu = Randu(0xDEADBEEF)
# lsfr = LFSR(0xDEADBEEF)
# glibc48 = Glibc(0x2197B942509FF4DB)
# quasirandom = Quasirandom()

generators = [
    # Linear Congruential Generators:
    Randu(seed1),
    Randu(seed2),
    Minstd(seed1),
    Minstd(seed2),
    Glibc(seed1),
    Glibc(seed2),
    pythonRandom(seed1),
    pythonRandom(seed2),
    FromBinaryFile("../pseudorandom-sequences/outjava.util.Random-seed1", 12000, "java.util.Random"),
    FromBinaryFile("../pseudorandom-sequences/outjava.util.Random-seed1", 12000, "java.util.Random"),
    FromBinaryFile("../pseudorandom-sequences/outjava.util.Random-seed2", 12000, "java.util.Random"),
    FromBinaryFile("../pseudorandom-sequences/outMWCNR-seed1", 12000, "MWCNR"),
    FromBinaryFile("../pseudorandom-sequences/outMWCNR-seed2", 12000, "MWCNR"),
    EICG1(seed1),
    EICG1(seed2),
    # Linear Feedback Shift Registers:
    LFSR(seed1),
    LFSR(seed2),
    FromBinaryFile("../pseudorandom-sequences/outXorShift32-seed1", 12000, "XorShift32"),
    FromBinaryFile("../pseudorandom-sequences/outXorShift32-seed2", 12000, "XorShift32"),
    FromBinaryFile("../pseudorandom-sequences/outXorShift-seed1", 12000, "XorShift64"),
    FromBinaryFile("../pseudorandom-sequences/outXorShift-seed2", 12000, "XorShift64"),
    # WELL generators:
    FromBinaryFile("../pseudorandom-sequences/outMersenneTwister-seed1", 12000, "MersenneTwister"),
    FromBinaryFile("../pseudorandom-sequences/outMersenneTwister-seed2", 12000, "MersenneTwister"),
    # Cryptographically Secure Generators:
    FromBinaryFile("../pseudorandom-sequences/outBlumBlumShub-seed1", 12000, "BlumBlubShub"),
    FromBinaryFile("../pseudorandom-sequences/outBlumBlumShub-seed2", 12000, "BlumBlubShub"),
    FromBinaryFile("../pseudorandom-sequences/outQCG631", 12000, "QCG631"),
    FromBinaryFile("../pseudorandom-sequences/outQCG651", 12000, "QCG651"),
    FromBinaryFile("../pseudorandom-sequences/outWebkit2", 12000, "Webkit2"),
    GameRand(seed1),
    FromBinaryFile("../pseudorandom-sequences/outPCG32", 12000, "PCG32"),
    FromBinaryFile("../pseudorandom-sequences/outRANROT", 12000, "Ranrot"),
    FromBinaryFile("../pseudorandom-sequences/outLamar", 12000, "Lamar"),
    FromBinaryFile("../pseudorandom-sequences/outRule30", 12000, "Rule30"),
    FromBinaryFile("../pseudorandom-sequences/outRANROT", 12000, "Ranrot"),
    # True Random:
    FromBinaryFile("../random-org-seq/TrueRandom2", 12000),
    FromBinaryFile("../random-org-seq/TrueRandom3", 12000),
    # Other:
    Quasirandom()
]
test = HypercubeTest(runs=10, number_of_points=12000, dimension=3, homology_dimension=0, filtration_size=40,
                     reference_rng=rng, scale=1)
test2 = HypercubeTest(runs=10, number_of_points=12000, dimension=3, homology_dimension=0, filtration_size=40,
                      reference_rng=rng, scale=0.45)
test3 = HypercubeTest(runs=10, number_of_points=12000, dimension=3, homology_dimension=0, filtration_size=40,
                      reference_rng=rng, scale=0.15)
test4 = HypercubeTest(runs=5, number_of_points=12000, dimension=3, homology_dimension=0, filtration_size=40,
                      reference_rng=rng, scale=0.075)

for generator in generators:
    test.visualise_failure(generator, "../visualisations/")
    test2.visualise_failure(generator, "../visualisations/")
    test3.visualise_failure(generator, "../visualisations/")
    test4.visualise_failure(generator, "../visualisations/")
# print("Scale:1.0")
# test.test_generator_list(generators)
# print("Scale:0.45")
# test2.test_generator_list(generators)
# print("Scale:0.15")
# test3.test_generator_list(generators)
# # print("Scale 0.075")
# test4.test_generator_list(generators)
