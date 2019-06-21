import os
import time

import numpy as np
from scipy import stats
from ripser import Rips
from typing import List
from scipy import sparse
from sklearn.metrics.pairwise import pairwise_distances

from src.pnrg import RNG, FromBinaryFile
from src.randology import visualise_point_cloud


def make_sparse_dm(points: np.array, thresh):
    n = points.shape[0]
    distance_matrix = pairwise_distances(points)
    [i, j] = np.meshgrid(np.arange(n), np.arange(n))
    i = i[distance_matrix <= thresh]
    j = j[distance_matrix <= thresh]
    v = distance_matrix[distance_matrix <= thresh]
    return sparse.coo_matrix((v, (i, j)), shape=(n, n)).tocsr()


def generate_points(rng: RNG, number_of_points, dimension, scale) -> np.array:
    """
    Generates a set of vectors in [0,1]^dimension hypercube.

    :param scale:
    :rtype: np.array
    :param rng: Random number pnrg to use.
    :param dimension: Dimension of the hypercube
    :param number_of_points: Number of vectors to generate
    :return: Array of vectors representing point cloud in a hypercube.
    """

    # points = []
    # for _ in range(self.number_of_points):
    #     point = []
    #     for _ in range(self.dimension):
    #         value = rng.next_float()
    #         while value > self.scale:
    #             value = rng.next_float()
    #         point.append(value)
    #     points.append(points)
    # return np.array(points)

    # function to generate a point.
    def generate_point(i, j):
        # i and j are required for np.fromfunction, but not used.
        del i, j
        value = rng.next_float()
        while value > scale:
            value = rng.next_float()
        return value

    # Then creates the array using said function.
    return np.fromfunction(np.vectorize(generate_point), (number_of_points, dimension))

    # return np.array([[rng.next_float() for _ in range(self.dimension)] for _ in range(self.number_of_points)])


class HypercubeTest:

    def __init__(self, reference_rng: RNG, number_of_points: int, runs: int = 10, dimension: int = 3,
                 scale: float = 1.0,
                 homology_dimension: int = 0,
                 filtration_size: int = 20, max_filtration_value: float = None):
        """
        Initialises a new HypercubeTest object.

        :rtype: None
        :param reference_rng: Random number pnrg to use to create a reference distribution.
        :param number_of_points: Number of points to generate for the point cloud.
        :param runs: How many times to run the test.
        :param dimension: The dimension of the hypercube to consider.
        :param homology_dimension: The maximum simplex dimension to be computed.
        :param filtration_size: Size of the filtration range to be used.
        :param max_filtration_value: The maximum value in the filtration, also the threshold value of the complex.
        """
        self.runs = runs
        self.number_of_points = number_of_points
        self.dimension = dimension
        self.homology_dimension = homology_dimension
        # self.filtration_range = np.array([0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.070, 0.075, 0.08, 0.085, 0.09, 0.095])
        # self.filtration_size = len(self.filtration_range)
        self.filtration_size = filtration_size
        self.scale = scale
        self.filtration_range = self.create_filtration_range(max_filtration_value)
        self.filtration = Rips(maxdim=self.homology_dimension, thresh=self.filtration_range[-1], verbose=True)
        self.reference_rng = reference_rng

    def generate_distribution(self, rng: RNG):
        """
        Takes the random number pnrg, and then generates the distribution of betti numbers for that RNG.RNG.

        Points are generated in the hypercube using the random number pnrg. Then the persistence diagram is
        calculated, and the betti numbers are then calculated from the persistence diagram.

        :rtype: np.array
        :param rng: random number pnrg to create a distribution for.
        :return: Array containing the betti numbers associated with each filtration value.
        """
        points = generate_points(rng, self.number_of_points, self.dimension, self.scale)
        # distance_matrix = pairwise_distances(points)
        sparse_distance_matrix = make_sparse_dm(points, self.filtration_range[-1])
        # An attempt to reduce memory usage, might not work
        del points
        diagrams = self.generate_diagrams(sparse_distance_matrix)
        homology = self.generate_homology(diagrams)
        return homology[self.homology_dimension]

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

    def single_run(self, rng: RNG, reference_distribution: np.array) -> float:
        """
        Performs a single iteration of the Unit Hypercube test, comparing the distribution generated by the given rng
        to the reference distribution. The comparison is done using the chi^2 test.

        :param rng: Random number pnrg to compare.
        :param reference_distribution: Distribution of betti numbers to compare against.
        :return: p value of the chi^2 test of comparing the two distributions.
        """
        observed_distribution = self.generate_distribution(rng)
        print(observed_distribution)
        return stats.chisquare(f_obs=observed_distribution, f_exp=reference_distribution)[1]

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

    def create_filtration_range(self, max_filtration_value) -> np.array:
        """
        Creates an evenly spaced interval to use as a range of filtration values.

        :return:
        :param max_filtration_value: optional specified maximum value to use in the range.
        :rtype: np.array
        :return: array containing the filtration range.
        """
        if max_filtration_value is not None:
            return np.linspace(0, max_filtration_value, self.filtration_size)
        if self.homology_dimension == 0:
            max_value = self.scale * 10 / (self.number_of_points ** (1.0 / self.dimension))
            return np.linspace(0, max_value, self.filtration_size)
        else:
            return np.linspace(0, self.scale * 1 / self.dimension, self.filtration_size)

    def visualise_failure(self, rng: RNG):
        point_cloud = generate_points(rng, self.number_of_points, self.dimension, self.scale)
        reference_point_cloud = generate_points(self.reference_rng, self.number_of_points, self.dimension, self.scale)
        diagram = self.generate_diagrams(pairwise_distances(reference_point_cloud))[self.homology_dimension]
        # This should be point before the diagram becomes fully connected.
        epsilon = 0
        for point in reversed(diagram):
            if not np.isinf(point[1]):
                epsilon = point[1]
                break
        filename = '../visualisations/{}-{}D-{}-{}.html'.format(rng.get_name(), self.dimension, self.number_of_points,
                                                                epsilon)
        visualise_point_cloud(point_cloud, epsilon, 10, filename)

    def test_directory(self, directory_path):
        generators = []
        for filename in os.listdir(directory_path):
            generators.append(FromBinaryFile(directory_path + '/' + filename, self.runs))
        self.test_generator_list(generators)

    def test_generator_list(self, generators):
        for rng in generators:
            start = time.time()
            passes = self.perform_test(rng)
            end = time.time()
            print('{}:{}/{}'.format(rng.get_name(), passes, self.runs))
            print("Time elapsed:", end - start)
        print("Done")
