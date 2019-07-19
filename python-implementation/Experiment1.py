import os
import sys
import time

import numpy as np
import matplotlib

from src.randology import *
from src.pnrg.LCGs import *
from src.pnrg.CSG import *
from src.pnrg.LFSRs import *
from src.pnrg.hash import *
from src.pnrg.other import MersenneTwister, Quasirandom
from src.pnrg import *
from src.pnrg.binary import *

seed1 = 0xDEADBEEF
seed2 = 0xD978757273


# rng2 = FromBinaryFile("../random-org-seq/TrueRandom2", 12000)
# fileRand = FromBinaryFile("../pseudo-random-sequences/outXorShift32", 12000)
# python_rand = pythonRandom("Python Random")
# gameRand = GameRand(0xDEADBEEF)
# randu = Randu(0xDEADBEEF)
# lsfr = LFSR(0xDEADBEEF)
# glibc48 = Glibc(0x2197B942509FF4DB)
# quasirandom = Quasirandom()
def get_reference_rng():
    return FromBinaryFile("../random-org-seq/TrueRandom1", 12000)


def get_generators():
    return [
        # Linear Congruential Generators:
        Randu(seed1),
        Randu(seed2),
        Minstd(seed1),
        Minstd(seed2),
        Glibc(seed1),
        Glibc(seed2),
        FromBinaryFile("../pseudorandom-sequences/outjava.util.Random-seed1", 12000, "java.util.Random"),
        FromBinaryFile("../pseudorandom-sequences/outjava.util.Random-seed2", 12000, "java.util.Random"),
        MWC(seed1),
        MWC(seed2),
        EICG1(seed1),
        EICG1(seed2),
        # Linear Feedback Shift Registers:
        LFSR(seed1),
        LFSR(seed2),
        XorShift32(seed1),
        XorShift32(seed2),
        XorShift64(seed1),
        XorShift64(seed2),
        Xorshift128p(seed1, seed2),
        # WELL generators:
        MersenneTwister(seed1),
        MersenneTwister(seed2),
        # Cryptographically Secure Generators:
        BlumBlumShub(seed1),
        BlumBlumShub(seed2),
        QCG631(seed1),
        QCG651(seed1),
        Webkit2(seed1),
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


test = HypercubeTest(runs=10, number_of_points=12000, dimension=3, homology_dimension=0, filtration_size=100,
                     reference_rng=get_reference_rng(), scale=1)
test2 = HypercubeTest(runs=10, number_of_points=12000, dimension=3, homology_dimension=0, filtration_size=100,
                      reference_rng=get_reference_rng(), scale=0.45)
test3 = HypercubeTest(runs=10, number_of_points=12000, dimension=3, homology_dimension=0, filtration_size=100,
                      reference_rng=get_reference_rng(), scale=0.15)
test4 = HypercubeTest(runs=5, number_of_points=12000, dimension=3, homology_dimension=0, filtration_size=100,
                      reference_rng=get_reference_rng(), scale=0.075)
# for generator in generators:
#     test.visualise_failure(generator, "../visualisations/")
#     test2.visualise_failure(generator, "../visualisations/")
#     test3.visualise_failure(generator, "../visualisations/")
#     test4.visualise_failure(generator, "../visualisations/")
print("Scale:1.0")
test.test_generator_list(get_generators())
print("Scale:0.45")
test2.test_generator_list(get_generators())
print("Scale:0.15")
test3.test_generator_list(get_generators())
print("Scale 0.075")
test4.test_generator_list(get_generators())
# test.test_generators_multiple_scales(get_generators(), scale_list=[0.15, 0.45, 1.0], failure_threshold=1)
