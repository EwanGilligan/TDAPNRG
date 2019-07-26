import time

from randology.pnrg import RNG
from .HomologyTest import HomologyTest
import numpy as np
from GF2Matrix import IntMatrix

np.set_printoptions(threshold=np.inf)


class MatrixRankTest(HomologyTest):

    def get_data_file_name(self) -> str:
        return '{}-{}-{}-{}'.format(self.__class__.__name__, self.matrix_size, self.number_of_points,
                                        int(time.time() * 1000))

    def generate_reference_distribution(self, reference_rng):
        # no extra steps for the reference distribution in this test.
        return self.generate_distribution(reference_rng, self.filtration_range)

    def __init__(self, reference_rng, runs, number_of_points, matrix_size=64, homology_dimension=0, filtration_size=5,
                 recalculate_distribution=False, store_data=False):
        assert matrix_size <= 64, "Matrix size must be a positive value less than or equal to 64."
        self.matrix_size = matrix_size
        super().__init__(reference_rng, runs, number_of_points, homology_dimension, filtration_size, matrix_size,
                         recalculate_distribution, store_data)

    def generate_distribution(self, rng, filtration_range):
        points = MatrixRankTest.generate_points(rng, self.number_of_points, self.matrix_size)
        dm = self.get_distance_matrix(points)
        diagrams = self.generate_diagrams(dm, filtration_range[-1])
        distribution = self.generate_homology(diagrams, filtration_range)[self.homology_dimension]
        if self.f is not None:
            output_string = "[Points]\n"
            for point in points:
                output_string += str(point) + "\n"
            output_string += "[Distance Matrix]\n"
            # convert to numpy array for nicer printing
            output_string += str(np.array(dm))
            output_string += "\n[Distribution]\n" + str(distribution) + "\n"
            self.f.write(output_string)
        return distribution

    def create_filtration_range(self):
        return [0, self.matrix_size - 3, self.matrix_size - 2, self.matrix_size - 1, self.matrix_size,
                self.matrix_size + 1]

    def get_distance_matrix(self, points):
        distances = np.ndarray((self.number_of_points, self.number_of_points))
        for i in range(self.number_of_points):
            for j in range(i + 1):
                # As the field is GF2, addition is the same as subtraction.
                distances[i][j] = distances[j][i] = (
                        points[i] + points[j]).rank()  # MatrixRankTest.rank_distance(points[i], points[j])
        return distances

    @staticmethod
    def rank_distance(m1, m2):
        t = m1 + m2
        return t.rank()

    @staticmethod
    def generate_points(rng: RNG, number_of_points, matrix_size):
        """
        Generate an array of m*m matrices with random entries from GF(2), where m is matrix_size.

        :param rng: Random number generator to use when generating the matrix entries.
        :param number_of_points: Number of matrices to generate.
        :param matrix_size: Size of matrix to generate. Note matrices are square.
        :return: Numpy array containing the matrices.
        """
        matrices = []
        for _ in range(number_of_points):
            matrices.append(MatrixRankTest.create_random_matrix(rng, matrix_size))
        return np.array(matrices)

    @staticmethod
    def create_random_matrix(rng: RNG, matrix_size):
        """
        Create a matrix_size*matrix_size with random entries from GF(2).

        :param rng: Random number generator to use when generating the matrix entries.
        :param matrix_size: Size of the matrix. Note the matrices are square.
        :return: GF2Matrix with random entries.
        """
        m = IntMatrix((matrix_size, matrix_size))
        for i in range(matrix_size):
            # Get a row vector of the 64 bits.
            # not sure why the cast to int is required, but get a type error otherwise.
            row_vector = [int(i) for i in np.binary_repr(int(rng.next_64_bits()), 64)]
            m.set_row(i, row_vector[0:matrix_size])
        return m
