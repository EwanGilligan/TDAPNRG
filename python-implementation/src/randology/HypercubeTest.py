

import numpy as np
# from scipy import stats
# from ripser import Rips
# from typing import List
from scipy import sparse
from scipy import spatial
from sklearn.metrics.pairwise import pairwise_distances

from src.pnrg import RNG, FromBinaryFile
from src.randology import plot_connected_components
from .HomologyTest import HomologyTest


class HypercubeTest(HomologyTest):

    def __init__(self, reference_rng: RNG, number_of_points: int, runs: int = 10, dimension: int = 3,
                 scale: float = 1.0, homology_dimension: int = 0, filtration_size: int = 20,
                 max_filtration_value: float = None, recalculate_distribution=False):
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
        self.dimension = dimension
        # self.filtration_range = np.array([0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.070, 0.075, 0.08, 0.085, 0.09, 0.095])
        # self.filtration_size = len(self.filtration_range)
        self.scale = scale
        super().__init__(reference_rng, runs, number_of_points, homology_dimension, filtration_size,
                         max_filtration_value, recalculate_distribution)

    def generate_distribution(self, rng: RNG):
        """
        Takes the random number pnrg, and then generates the distribution of betti numbers for that RNG.RNG.

        Points are generated in the hypercube using the random number pnrg. Then the persistence diagram is
        calculated, and the betti numbers are then calculated from the persistence diagram.

        :rtype: np.array
        :param rng: random number pnrg to create a distribution for.
        :return: Array containing the betti numbers associated with each filtration value.
        """
        points = self.generate_points(rng, self.number_of_points, self.dimension, self.scale)
        # distance_matrix = pairwise_distances(points)
        sparse_distance_matrix = self.make_sparse_dm(points, self.filtration_range[-1])
        # An attempt to reduce memory usage, might not work
        del points
        diagrams = self.generate_diagrams(sparse_distance_matrix)
        homology = self.generate_homology(diagrams)
        return homology[self.homology_dimension]

    def create_filtration_range(self, max_filtration_value=None) -> np.array:
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
            max_value = self.scale * (2 / self.number_of_points ** (1.0 / self.dimension))
            return np.linspace(0, max_value, self.filtration_size)
        else:
            return np.linspace(0, self.scale * 1 / self.dimension, self.filtration_size)

    def visualise_failure(self, rng: RNG, filepath: str):
        point_cloud = self.generate_points(rng, self.number_of_points, self.dimension, self.scale)
        reference_point_cloud = self.generate_points(self.reference_rng, self.number_of_points, self.dimension,
                                                     self.scale)
        diagram = self.generate_diagrams(pairwise_distances(reference_point_cloud))[self.homology_dimension]
        # This should be point before the diagram becomes fully connected.
        epsilon = 0
        for point in reversed(diagram):
            if not np.isinf(point[1]):
                epsilon = point[1]
                break
        filename = '{}-{}D-{}-{}'.format(rng.get_name(), self.dimension, self.number_of_points,
                                              self.scale)
        plot_connected_components(point_cloud, epsilon, filename, filepath, 20)

    @staticmethod
    def make_sparse_dm(points: np.array, thresh):
        n = points.shape[0]
        distance_matrix = spatial.distance.squareform(spatial.distance.pdist(points)) #pairwise_distances(points)
        [i, j] = np.meshgrid(np.arange(n), np.arange(n))
        i = i[distance_matrix <= thresh]
        j = j[distance_matrix <= thresh]
        v = distance_matrix[distance_matrix <= thresh]
        return sparse.coo_matrix((v, (i, j)), shape=(n, n)).tocsr()

    @staticmethod
    def generate_points(rng: RNG, number_of_points, dimension, scale=1.0) -> np.array:
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
