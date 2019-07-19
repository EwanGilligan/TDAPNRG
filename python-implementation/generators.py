from src.randology import *
from src.pnrg.LCGs import *
from src.pnrg.CSG import *
from src.pnrg.LFSRs import *
from src.pnrg.hash import *
from src.pnrg.other import MersenneTwister, Quasirandom
from src.pnrg import *
from src.pnrg.binary import *

LCGs = ['Randu', 'Minstd', 'Glibc', 'MWC', 'EICG1']
LFSRs = ['LFSR', 'XorShift32', 'XorShift64', 'Xorshift128+', 'Xoroshiro256+', 'Xoshiro256**']

generator_group_dict = {
    'LCGs': LCGs,
    'LFSRs': LFSRs
}


def get_generator_dict(seeds):
    """
    Returns a dictionary containing generators
    :param seeds: list of values to use as the seed of the generators.
    :return: dict where the keys are the names of the random number generators, and the values are the generators.
    """
    return {
        # linear congruential generators.
        'Randu': Randu(seeds[1]),
        'Minstd': Minstd(seeds[1]),
        'Glibc': Glibc(seeds[1]),
        'java.util.Random': FromBinaryFile("../pseudorandom-sequences/outjava.util.Random-seed1", 12000,
                                           "java.util.Random"),
        'MWC': MWC(seeds[1]),
        'EICG1': EICG1(seeds[1]),
        # Linear Feedback Shift Registers:
        'LFSR': LFSR(seeds[1]),
        'XorShift32': XorShift32(seeds[1]),
        'XorShift64': XorShift64(seeds[1]),
        'Xorshift128+': Xorshift128p(seeds[1], seeds[2]),
        'Xoroshiro256+': Xoshiro256p(seeds),
        'Xoshiro256**': Xoshiro256ss(seeds),
        # WELL generators:
        'MersenneTwister': MersenneTwister(seeds[1]),
        # Cryptographically Secure Generators:
        'BlumBlumShub': BlumBlumShub(seeds[1]),
        'QCG631': QCG631(seeds[1]),
        'QCG651': QCG651(seeds[1]),
        'Webkit2': Webkit2(seeds[1]),
        'GamrRand': GameRand(seeds[1]),
        'PCG32': FromBinaryFile("../pseudorandom-sequences/outPCG32", 12000, "PCG32"),
        'Ranrot': FromBinaryFile("../pseudorandom-sequences/outRANROT", 12000, "Ranrot"),
        'Lamar': FromBinaryFile("../pseudorandom-sequences/outLamar", 12000, "Lamar"),
        'Rule30': FromBinaryFile("../pseudorandom-sequences/outRule30", 12000, "Rule30"),
        # True Random:
        'TrueRandom2': FromBinaryFile("../random-org-seq/TrueRandom2", 12000),
        'TrueRandom3': FromBinaryFile("../random-org-seq/TrueRandom3", 12000),
        # Other:
        'Quasirandom': Quasirandom()
    }


def get_generator_list(generator_list, seeds):
    generator_dict = get_generator_dict(seeds)
    return map(generator_dict.__getitem__, generator_list)


def generator_group(group):
    """
    Creates a curried function that will return the specified group, when provided with seeds.
    :param group: Name of the group to return.
    :return: a function that takes the generator seeds, and returns an iterable of generators.
    """
    if group == 'fulltest':
        def get_full_test(seeds):
            return get_generator_dict(seeds).values()

        return get_full_test

    def get_subgroup(seeds):
        return get_generator_list(generator_group_dict[group], seeds)

    return get_subgroup
