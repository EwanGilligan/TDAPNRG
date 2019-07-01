from abc import ABC, abstractmethod

import os
import time

import numpy as np
from scipy import stats
from ripser import Rips
from typing import List

from pnrg import RNG, FromBinaryFile


class HomologyTest(ABC):
    def __init__(self, reference_rng, runs, homology_dimension, filtration_size, filtration_value):
        self.reference_rng = reference_rng
        self.runs = runs
        self.homology_dimension = homology_dimension
        self.filtration_size = filtration_size
        self.filtration_range = self.create_filtration_range(filtration_value)
        self.filtration = Rips(maxdim=self.homology_dimension, thresh=self.filtration_range[-1], verbose=True)

    def generate_diagrams(self, distance_matrix) -> List[np.ndarray]:
        """
        Generates the persistence diagrams from the given distance matrix.

        :param distance_matrix: distance matrix of the point cloud.
        :rtype: dict
        :return: A list of persistence diagrams,  one for each dimension less than maximum homology dimension.
        Each diagram is an ndarray of size (n_pairs, 2) with the first column representing the birth time and
        the second column representing the death time of each pair.
        """
        diagrams = self.filtration.fit_transform(distance_matrix, distance_matrix=True)
        return diagrams

    def generate_homology(self, diagrams):
        """
        Generate tbe betti numbers associated with the diagrams.

        :param diagrams: dictionary with entries for each dimension less than homology dimension, with each entry being
        the persistence diagram for that dimension.
        :return: dictionary containing entries for each dimension less than homology dimension, with each entry being a
        list of the betti numbers for each value in the filtration range.
        """
        homology = {dimension: np.zeros(self.filtration_size) for dimension in range(self.homology_dimension + 1)}
        for dimension, diagram, in enumerate(diagrams):
            if dimension <= self.homology_dimension and len(diagram) > 0:
                homology[dimension] = np.array(
                    [np.array(((self.filtration_range >= point[0]) & (self.filtration_range <= point[1]))).astype(int)
                     for point
                     in diagram]).sum(axis=0).tolist()
        return homology

    def perform_test(self, rng: RNG) -> int:
        """
        Performs multiple runs of the Unit Hypercube test. The number of runs is specified when the HypercubeTest object
        is initialised. The test is passed if the p value of the single run is greater than 0.01, and this counts the
        number of passes.

        :param rng: Random number pnrg to test.
        :return: Number of times the rng passes the test.
        """
        passes = 0
        reference_distribution = self.generate_distribution(self.reference_rng)
        for i in range(self.runs):
            # if the p value is greater than 0.01
            if self.single_run(rng, reference_distribution) > 0.01:
                passes += 1
        return passes

    def single_run(self, rng: RNG, reference_distribution: np.array) -> float:
        """
        Performs a single iteration of the implemented Homology Test, comparing the distribution generated by the given rng
        to the reference distribution. The comparison is done using the chi^2 test.

        :param rng: Random number pnrg to compare.
        :param reference_distribution: Distribution of betti numbers to compare against.
        :return: p value of the chi^2 test of comparing the two distributions.
        """
        observed_distribution = self.generate_distribution(rng)
        return stats.chisquare(f_obs=observed_distribution, f_exp=reference_distribution)[1]

    @abstractmethod
    def generate_distribution(self, reference_rng):
        pass

    @abstractmethod
    def create_filtration_range(self, filtration_value):
        pass

    @staticmethod
    @abstractmethod
    def generate_points(rng: RNG):
        pass

    def test_directory(self, directory_path):
        """
        Perform the Unit Hypercube Test on a directory of binary files that are the output to a RNG.

        :param directory_path: Path to the directory containing the binary files.
        """
        generators = []
        for filename in os.listdir(directory_path):
            generators.append(FromBinaryFile(directory_path + '/' + filename, self.runs))
        self.test_generator_list(generators)

    def test_generator_list(self, generators) -> None:
        """
        Takes and list of RNGs and then performs the Unit Hypercube test on all of them, printing the result of each
        test to the console. The time taken for each test is also printed.

        :param generators: Iterable object containing a list of RNG type objects to be tested.
        """
        for rng in generators:
            start = time.time()
            passes = self.perform_test(rng)
            end = time.time()
            print('{}:{}/{}'.format(rng.get_name(), passes, self.runs))
            print("Time elapsed:", end - start)
        print("Done")