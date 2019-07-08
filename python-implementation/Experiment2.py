from src.pnrg import FromBinaryFile
from src.pnrg.LCGs import *
from src.pnrg.CSG import *
from src.pnrg.LFSR import LFSR
from src.pnrg import Quasirandom, pythonRandom, FromBinaryFile
from src.randology import MatrixRankTest

seed1 = 0xDEADBEEF
seed2 = 0xD978757273


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
        pythonRandom(seed1),
        pythonRandom(seed2),
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


test = MatrixRankTest(reference_rng=get_reference_rng(), runs=10, matrix_size=64, homology_dimension=0,
                      filtration_size=5, number_of_points=100)
test.test_generator_list(get_generators())
