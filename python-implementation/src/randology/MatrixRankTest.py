from pnrg import RNG
from .HomologyTest import HomologyTest
from typing import Tuple
import numpy as np
from sklearn.metrics import pairwise_distances
from GF2Matrix import IntMatrix


class MatrixRankTest(HomologyTest):

    def generate_reference_distribution(self, reference_rng):
        return self.generate_distribution(reference_rng, self.filtration_range)

    def __init__(self, reference_rng, runs, number_of_points, matrix_size=64, homology_dimension=1, filtration_size=5,
                 recalculate_distribution=False):
        assert matrix_size <= 64, "Matrix size must be a positive value less than or equal to 64."
        self.matrix_size = matrix_size
        super().__init__(reference_rng, runs, number_of_points, homology_dimension, filtration_size, matrix_size,
                         recalculate_distribution)

    def generate_distribution(self, rng, filtration_range):
        points = MatrixRankTest.generate_points(rng, self.number_of_points, self.matrix_size)
        dm = self.get_distance_matrix(points)
        diagrams = self.generate_diagrams(dm, filtration_range[-1])
        return self.generate_homology(diagrams, filtration_range)[self.homology_dimension]

    def create_filtration_range(self):
        return [0, self.matrix_size - 3, self.matrix_size - 2, self.matrix_size - 1, self.matrix_size,
                self.matrix_size + 1]

    def get_distance_matrix(self, points):
        distances = np.ndarray((self.number_of_points, self.number_of_points))
        for i in range(self.number_of_points):
            for j in range(i + 1):
                distances[i][j] = distances[j][i] = MatrixRankTest.rank_distance(points[i], points[j])
        return distances

    @staticmethod
    def rank_distance(m1, m2):
        t = m1 + m2
        return t.rank()

    @staticmethod
    def generate_points(rng: RNG, number_of_points, matrix_size):
        matrices = []
        for _ in range(number_of_points):
            matrices.append(MatrixRankTest.create_random_matrix(rng, matrix_size))
        return np.array(matrices)

    @staticmethod
    def create_random_matrix(rng: RNG, matrix_size):
        m = IntMatrix((matrix_size, matrix_size))
        for i in range(matrix_size):
            # Get a row vector of the 64 bits.
            # not sure why the cast to int is required, but get a type error otherwise.
            row_vector = [int(i) for i in np.binary_repr(int(rng.next_64_bits()), 64)]
            m.set_row(i, row_vector[0:matrix_size])
        return m
