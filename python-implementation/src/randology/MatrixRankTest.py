from pnrg import RNG
from .HomologyTest import HomologyTest
from pyfinite import genericmatrix, ffield
from typing import Tuple
import numpy as np
from sklearn.metrics import pairwise_distances


class MatrixRankTest(HomologyTest):

    def __init__(self, reference_rng, runs, number_of_points, matrix_size=64, homology_dimension=1, filtration_size=5,
                 filtration_value=None):
        assert matrix_size <= 64, "Matrix size must be a positive value less than or equal to 64."
        super().__init__(reference_rng, runs, number_of_points, homology_dimension, filtration_size, matrix_size)
        self.matrix_size = matrix_size

    def generate_distribution(self, rng):
        points = MatrixRankTest.generate_points(rng, self.number_of_points, self.matrix_size)
        dm = self.get_distance_matrix(points)
        diagrams = self.generate_diagrams(dm)
        return self.generate_homology(diagrams)[self.homology_dimension]

    def create_filtration_range(self, matrix_size):
        return [0, matrix_size - 3, matrix_size - 2, matrix_size - 1, matrix_size,
                matrix_size + 1]

    def get_distance_matrix(self,points):
        distances = np.ndarray((self.number_of_points, self.number_of_points))
        for i in range(self.number_of_points):
            for j in range(i + 1):
                distances[i][j] = distances[j][i] = MatrixRankTest.rank_distance(points[i], points[j])
        return distances


    @staticmethod
    def rank_distance(m1, m2):
        t = m1 + m2
        return MatrixRankTest.rank(t)

    @staticmethod
    def generate_points(rng: RNG, number_of_points, matrix_size):
        matrices = []
        for _ in range(number_of_points):
            matrices.append(MatrixRankTest.create_random_matrix(rng, matrix_size))
        return np.array(matrices)

    @staticmethod
    def create_random_matrix(rng: RNG, matrix_size):
        m = MatrixRankTest.create_GF2_matrix((matrix_size, matrix_size))
        for i in range(matrix_size):
            # Get a row vector of the 64 bits.
            # not sure why the cast to int is required, but get a type error otherwise.
            row_vector = [int(i) for i in np.binary_repr(int(rng.next_64_bits()), 64)]
            m.SetRow(i, row_vector[0:matrix_size])
        return m

    @staticmethod
    def rank(matrix: genericmatrix.GenericMatrix):
        # Perform lower gaussian elimination
        matrix.LowerGaussianElim()
        rank = matrix.rows
        # Iterate over the rows in reverse order.
        for i in reversed(range(matrix.rows)):
            # If the row contains 1, then stop
            if 1 in matrix.GetRow(i):
                break
            # Otherwise the row is a zero row and so the rank is reduced by 1.
            rank -= 1
        return rank

    @staticmethod
    def create_GF2_matrix(size: Tuple[int, int] = (2, 2)):
        """
        Wrapper function to create a GF2 matrix.
        :param size: Size of the matrix to create.
        :return: GenericMatrix, that will perform its operations over GF2
        """
        XOR = lambda x, y: x ^ y
        AND = lambda x, y: x & y
        DIV = lambda x, y: x
        return genericmatrix.GenericMatrix(size, zeroElement=0, identityElement=1, add=XOR, mul=AND, sub=XOR, div=DIV)
