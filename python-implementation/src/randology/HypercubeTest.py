import gc

import numpy as np
from scipy import stats
from ripser import Rips
from typing import List
from scipy import sparse
from sklearn.metrics.pairwise import pairwise_distances

from src.generator import RNG
from src.randology.visualiser import visualise_point_cloud


def make_spare_dm(points, thresh):
    m = points.shape[0]
    n = points.shape[1]
    d = pairwise_distances(points, metric='euclidean')
    [i, j] = np.meshgrid(np.arange(n))
    i = i[d <= thresh]
    j = j[d <= thresh]
    v = d[d <= thresh]
    return sparse.coo_matrix((v, (i, j)), shape=(m, n)).tocsr()


def generate_points(rng: RNG, dimension: int, number_of_points: int) -> np.array:
    """
    Generates a set of vectors in [0,1]^dimension hypercube.

    :rtype: np.array
    :param rng: Random number generator to use.
    :param dimension: Dimension of the hypercube
    :param number_of_points: Number of vectors to generate
    :return: Array of vectors representing point cloud in a hypercube.
    """
    return np.array([[rng.next_float() for _ in range(dimension)] for _ in range(number_of_points)])


class HypercubeTest:

    def __init__(self, reference_rng: RNG, number_of_points: int, runs: int = 10, dimension: int = 3,
                 homology_dimension: int = 0,
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
        self.reference_rng = reference_rng

    def generate_distribution(self, rng: RNG):
        """
        Takes the random number generator, and then generates the distribution of betti numbers for that RNG.

        Points are generated in the hypercube using the random number generator. Then the persistence diagram is
        calculated, and the betti numbers are then calculated from the persistence diagram.

        :rtype: np.array
        :param rng: random number generator to create a distribution for.
        :return: Array containing the betti numbers associated with each filtration value.
        """
        points = generate_points(rng, self.dimension, self.number_of_points)
        diagrams = self.generate_diagrams(points)
        # An attempt to reduce memory usage, might not work
        del points
        gc.collect()
        homology = self.generate_homology(diagrams)
        return homology[self.homology_dimension]

    def generate_diagrams(self, points: np.array) -> List[np.ndarray]:
        """
        Generates the persistence diagrams from the given point cloud.

        :rtype: dict
        :param points: Point cloud to generate diagram for.
        :return: A list of persistence diagrams,  one for each dimension less than maximum homology dimension.
        Each diagram is an ndarray of size (n_pairs, 2) with the first column representing the birth time and
        the second column representing the death time of each pair.
        """
        filtration = Rips(maxdim=self.homology_dimension, thresh=self.filtration_range[-1], verbose=True)
        diagrams = filtration.fit_transform(points)
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

        :param rng: Random number generator to compare.
        :param reference_distribution: Distribution of betti numbers to compare against.
        :return: p value of the chi^2 test of comparing the two distributions.
        """
        observed_distribution = self.generate_distribution(rng)
        return stats.chisquare(f_obs=observed_distribution, f_exp=reference_distribution)[1]

    def perform_test(self, rng: RNG) -> int:
        """
        Performs multiple runs of the Unit Hypercube test. The number of runs is specified when the HypercubeTest object
        is initialised. The test is passed if the p value of the single run is greater than 0.01, and this counts the
        number of passes.

        :param rng: Random number generator to test.
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
            max_value = 10.0 / (self.number_of_points ** (1.0 / self.dimension))
            return np.linspace(0, max_value, self.filtration_size)
        else:
            return np.linspace(0, 1 / self.dimension, self.filtration_size)

    def visualise_failure(self, rng: RNG):
        point_cloud = generate_points(rng, self.dimension, self.number_of_points)
        reference_point_cloud = generate_points(self.reference_rng, self.dimension, self.number_of_points)
        diagram = self.generate_diagrams(reference_point_cloud)[self.homology_dimension]
        # This should be point before the diagram becomes fully connected.
        epsilon = diagram[-2][1]
        filename = '../visualisations/{}-{}D-{}-{}.html'.format(rng.get_name(), self.dimension, self.number_of_points, epsilon)
        visualise_point_cloud(point_cloud, epsilon, 10, filename)
