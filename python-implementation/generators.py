import os
from typing import List, Iterable, Callable, Dict
import numpy as np
from randology.pnrg.CSG import *
from randology.pnrg.hash import *
from randology.pnrg.other import MersenneTwister, Quasirandom
from randology.pnrg.binary import *
from randology.pnrg.LFSRs import *
from randology.pnrg.LCGs import *
from randology.pnrg import RNG
import gdown

LCGs = ['Randu', 'Minstd', 'Glibc', 'MWC', 'EICG1']
LFSRs = ['LFSR', 'XorShift32', 'XorShift64', 'Xorshift128+', 'Xoroshiro256+', 'Xoshiro256**']

generator_group_dict = {
    'LCGs': LCGs,
    'LFSRs': LFSRs
}


def get_generator_dict(seeds: List[int], salt: str = None) -> Dict[str, RNG]:
    """
    Returns a dictionary containing generators
    :param salt: A salt for the hashing algorithms. These won't be included if no salt is provided.
    :param seeds: list of values to use as the seed of the generators.
    :return: dict where the keys are the names of the random number generators, and the values are the generators.
    """
    seed1 = seeds[0]
    seed2 = seeds[1]
    dict = {
        # linear congruential generators.
        'Randu': Randu(seed1),
        'Minstd': Minstd(seed1),
        'Glibc': Glibc(seed1),
        # 'java.util.Random': FromBinaryFile("../pseudorandom-sequences/outjava.util.Random-seed1", 12000,
        #                                    "java.util.Random"),
        'MWC': MWC(seed1),
        'EICG1': EICG1(seed1),
        # Linear Feedback Shift Registers:
        'LFSR': LFSR(seed1),
        'XorShift32': XorShift32(seed1),
        'XorShift64': XorShift64(seed1),
        'Xorshift128+': Xorshift128p(seed1, seed2),
        'Xoroshiro256+': Xoshiro256p(np.array(seeds, dtype=np.int64)),
        'Xoshiro256**': Xoshiro256ss(np.array(seeds, dtype=np.int64)),
        # WELL generators:
        'MersenneTwister': MersenneTwister(seed1),
        # Cryptographically Secure Generators:
        'BlumBlumShub': BlumBlumShub(seed1),
        'QCG631': QCG631(seed1),
        'QCG651': QCG651(seed1),
        'Webkit2': Webkit2(seed1),
        'GamrRand': GameRand(seed1),
        # 'PCG32': FromBinaryFile("../pseudorandom-sequences/outPCG32", 12000, "PCG32"),
        # 'Ranrot': FromBinaryFile("../pseudorandom-sequences/outRANROT", 12000, "Ranrot"),
        # 'Lamar': FromBinaryFile("../pseudorandom-sequences/outLamar", 12000, "Lamar"),
        # 'Rule30': FromBinaryFile("../pseudorandom-sequences/outRule30", 12000, "Rule30"),
        # True Random:
        # 'TrueRandom2': FromBinaryFile("../random-org-seq/TrueRandom2", 12000),
        # 'TrueRandom3': FromBinaryFile("../random-org-seq/TrueRandom3", 12000),
        # Other:
        'Quasirandom': Quasirandom()
    }
    # if a salt is provided.
    if salt is not None:
        dict.update({
            # hashing algorithm generators.
            "SHA256": SHA256(seed1, salt),
            "SHA512": SHA512(seed1, salt),
            "SHA384": SHA384(seed1, salt),
            "SHA1": SHA1(seed1, salt)

        })
    return dict


def get_generator_list(generator_list: Iterable[str], seeds: List[int], salt: str = None) -> Iterable[RNG]:
    """
    Takes a list of generators and seeds for the generators, and then creates an iterable of the specified generators.

    :param salt:
    :param generator_list: List of names of generators to test.
    :param seeds: Indexable of seeds for the generators.
    :return: iterable of RNGs
    """
    generator_dict = get_generator_dict(seeds)
    return map(generator_dict.__getitem__, generator_list)


def generator_group(group: str, salt: str = None) -> Callable[[Iterable], Iterable[RNG]]:
    """
    Creates a curried function that will return the specified group, when provided with seeds.
    :param salt:
    :param group: Name of the group to return.
    :return: a function that takes the generator seeds, and returns an iterable of generators.
    """
    if group == 'fulltest':
        def get_full_test(seeds):
            return iter(get_generator_dict(seeds, salt).values())

        return get_full_test

    def get_subgroup(seeds):
        return get_generator_list(generator_group_dict[group], seeds, salt)

    return get_subgroup


def download_directory(url: str, directory: str, verbose: bool = True):
    filename = directory + "download.zip"
    gdown.download(url, filename, quiet=not verbose)
    gdown.extractall(filename)


def download_generator(url: str, filepath: str, size: int, loop_file: bool = True, verbose: bool = True) -> RNG:
    filepath = gdown.download(url, filepath, quiet=not verbose)
    return FromBinaryFile(filepath, size=size, loop_file=loop_file)


def get_generators_from_directory(directory_path: str, size: int, loop_file: bool = True) -> Iterable[RNG]:
    """
    Create a list of generators from a directory containing binary files.
    :param loop_file: Whether or not the generator will loop back to the start of the file.
    :param directory_path: Path to the directory.
    :param size: Size of the buffer to use for the generator.
    :return: List of RNGS
    """
    generators = []
    for filename in os.listdir(directory_path):
        # don't use the downloaded file.
        if filename.endswith(".zip"):
            continue
        generators.append(FromBinaryFile(directory_path + filename, size, name=filename, loop_file=loop_file))
    return iter(generators)
