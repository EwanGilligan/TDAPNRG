import gc

import numpy as np
from scipy import stats
from ripser import Rips
from typing import List
from scipy import sparse
from sklearn.metrics.pairwise import pairwise_distances

from src.generator import RNG


def make_spare_dm(points, thresh):
    m = points.shape[0]
    n = points.shape[1]
    d = pairwise_distances(points, metric='euclidean')
    [i, j] = np.meshgrid(np.arange(n))
    i = i[d <= thresh]
    j = j[d <= thresh]
    v = d[d <= thresh]
    return sparse.coo_matrix((v, (i, j)), shape=(m, n)).tocsr()


class HypercubeTest:

    def __init__(self, reference_rng: RNG, number_of_points: int, runs: int = 10, dimension: int = 3,
                 homology_dimension: int = 1,
                 filtration_size: int = 20, max_filtration_value: float = None):
        """
        Initialises a new HypercubeTest object.

        :rtype: None
        :param reference_rng: Random number generator to use to create a reference distribution.
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
        self.filtration_range = self.create_filtration_range(max_filtration_value)
        self.reference_distribution = self.generate_distribution(reference_rng)

    def generate_distribution(self, rng: RNG):
        points = self.generate_points(rng)
        diagrams = self.generate_diagram(points)
        del points
        gc.collect()
        homology = self.generate_homology(diagrams)
        return homology[0]

    def generate_diagram(self, points: np.array) -> List[np.ndarray]:
        filtration = Rips(maxdim=self.homology_dimension, thresh=self.filtration_range[-1], verbose=True)
        diagrams = filtration.fit_transform(points)
        return diagrams

    def generate_points(self, rng: RNG) -> np.array:
        return np.array([[rng.next_float() for _ in range(self.dimension)] for _ in range(self.number_of_points)])

    def generate_homology(self, diagrams):
        homology = {dimension: np.zeros(self.filtration_size) for dimension in range(self.homology_dimension + 1)}
        for dimension, diagram, in enumerate(diagrams):
            if dimension <= self.homology_dimension and len(diagram) > 0:
                homology[dimension] = np.array(
                    [np.array(((self.filtration_range >= point[0]) & (self.filtration_range <= point[1])).astype(int))
                     for point
                     in diagram]).sum(axis=0).tolist()
        return homology

    def single_run(self, rng: RNG):
        observed_distribution = self.generate_distribution(rng)
        return stats.chisquare(f_obs=observed_distribution, f_exp=self.reference_distribution)[1]

    def perform_test(self, rng: RNG):
        passes = 0
        for i in range(self.runs):
            if self.single_run(rng) > 0.01:
                passes += 1
        return passes

    def create_filtration_range(self, max_filtration_value) -> np.array:
        """
        Creates an evenly spaced interval to use as a range of filtration values.

        :param max_filtration_value:
        :rtype: np.array
        :param n: Number of values in the filtration (20 by default).
        :param max_value: The maximum value in the filtration range.
        :return: array containing the filtration range.
        """
        if max_filtration_value is not None:
            return np.linspace(0, max_filtration_value, self.filtration_size)
        if self.homology_dimension == 0:
            max_value = 10.0 / (self.number_of_points ** (1.0 / self.dimension))
            return np.linspace(0, max_value, self.filtration_size)
        else:
            return np.linspace(0, 1 / self.dimension, self.filtration_size)
