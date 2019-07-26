import numpy as np
from scipy import sparse
from scipy import spatial
import time

from randology.pnrg import RNG
from src.randology import visualise_connected_components_animated
from .HomologyTest import HomologyTest

np.set_printoptions(threshold=np.inf)


class HypercubeTest(HomologyTest):

    def get_data_file_name(self) -> str:
        return '{}-{}-{}-{}'.format(self.__class__.__name__, self.dimension, self.number_of_points,
                                    int(time.time() * 1000))

    def generate_reference_distribution(self, reference_rng):
        # generate points at a scale of 1.0
        filtration_range = self.create_filtration_range(scale=1)
        return self.generate_distribution(reference_rng, filtration_range=filtration_range, scale=1)

    def __init__(self, reference_rng: RNG, number_of_points: int, runs: int = 10, dimension: int = 3,
                 scale: float = 1.0, homology_dimension: int = 0, filtration_size: int = 20,
                 max_filtration_value: float = None, recalculate_distribution=False, delayed_coordinates=False,
                 store_data=False, gpu=False):
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
                         max_filtration_value, recalculate_distribution, store_data, gpu)
        # Delayed coordinates can only be used for 3D. Working on making it more general.
        assert not delayed_coordinates or (
                delayed_coordinates and dimension == 3), "Delayed coordinates can only be used for 3D."
        self.delayed_coordinates = delayed_coordinates

    def generate_distribution(self, rng: RNG, filtration_range, scale=None):
        """
        Takes the random number pnrg, and then generates the distribution of betti numbers for that RNG.RNG.

        Points are generated in the hypercube using the random number pnrg. Then the persistence diagram is
        calculated, and the betti numbers are then calculated from the persistence diagram.

        :param scale:
        :param filtration_range:
        :rtype: np.array
        :param rng: random number pnrg to create a distribution for.
        :return: Array containing the betti numbers associated with each filtration value.
        """
        if scale is None:
            scale = self.scale
        if self.delayed_coordinates:
            points = self.generate_3D_points_delayed(rng, self.number_of_points, scale)
        else:
            points = self.generate_points(rng, self.number_of_points, self.dimension, scale)
        # distance_matrix = pairwise_distances(points)
        if self.gpu:
            # TODO add  in GPU calculation.
            raise NotImplementedError("GPU calculation of distance matrix not implemented yet.")
        else:
            sparse_distance_matrix = self.make_sparse_dm(points, filtration_range[-1])
        if self.f is not None:
            output_string = "[Points]\n"
            output_string += str(points)
            self.f.write(output_string)
        # An attempt to reduce memory usage, might not work
        del points
        diagrams = self.generate_diagrams(sparse_distance_matrix, threshold=filtration_range[-1])
        homology = self.generate_homology(diagrams, filtration_range)
        distribution = homology[self.homology_dimension]
        if self.f is not None:
            self.f.write("\n[Distribution]\n" + str(distribution) + "\n")
        return distribution

    def create_filtration_range(self, scale=None, max_filtration_value=None) -> np.array:
        """
        Creates an evenly spaced interval to use as a range of filtration values.

        :param scale:
        :return:
        :param max_filtration_value: optional specified maximum value to use in the range.
        :rtype: np.array
        :return: array containing the filtration range.
        """
        if scale is None:
            scale = self.scale
        if max_filtration_value is not None:
            return np.linspace(0, max_filtration_value, self.filtration_size)
        if self.homology_dimension == 0:
            # for rational behind approximation, see https://arxiv.org/abs/math/0212230
            max_value = scale * (2 / self.number_of_points ** (1.0 / self.dimension))
            return np.linspace(0, max_value, self.filtration_size)
        else:
            return np.linspace(0, scale * 1 / self.dimension, self.filtration_size)

    def visualise_failure(self, rng: RNG, filepath: str):
        point_cloud = self.generate_points(rng, self.number_of_points, self.dimension, self.scale)
        visualise_connected_components_animated(point_cloud, rng.get_name(), filepath, self.filtration_range)

    @staticmethod
    def make_sparse_dm(points: np.array, thresh):
        n = points.shape[0]
        distance_matrix = spatial.distance.squareform(spatial.distance.pdist(points))  # pairwise_distances(points)
        [i, j] = np.meshgrid(np.arange(n), np.arange(n))
        points_under_thresh = distance_matrix <= thresh
        i = i[points_under_thresh]
        j = j[points_under_thresh]
        v = distance_matrix[points_under_thresh]
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

    @staticmethod
    def generate_3D_points_delayed(rng: RNG, number_of_points, scale=1.0):
        # function to generate point in scale.
        def generate_point():
            value = rng.next_float()
            while value > scale:
                value = rng.next_float()
            return value

        points = []
        for _ in range(number_of_points):
            x = generate_point()  # s[n-3]
            y = generate_point()  # s[n -2]
            z = generate_point()  # s[n -1]

            x = y - x  # s{n-2] - s[n-3]
            y = z - y  # s[n-1] - s[n-2]
            z = generate_point() - z  # s[n] - s[n-1]
            # normalise points to unit hypercube
            point = np.array([x, y, z])
            point = 0.5 * (point + scale)
            points.append(point)
        return np.array(points)

    def test_generators_multiple_scales(self, generators, scale_list=None, failure_threshold=0, verbose=True):
        """
        Tests a list of generators, at multiple scales. Generators are removed from the list if the fail the test a specified number of times.

        :param generators: List of random number generators.
        :param scale_list: List of scales to test at.
        :param failure_threshold: If a generator fails the test at least this many times, then it will be removed from subsequent testing.
        :param verbose: Whether or not intermediate test results are printed.
        :return: dictionary containing each random number generator, and the scale at which they last passed the test.
        If the generator passes at no scales, then -1 is there.
        """
        # -1 indicates a pass at no scales.
        results_dict = {rng.get_name(): {
            'max_scale': -1,
            'results': []
        } for rng in generators}
        total_start = time.time()
        original_scale = self.scale
        if scale_list is None:
            scale_list = [1.0]
        for scale in scale_list:
            # break if no more generators.
            if len(generators) == 0:
                break
            if verbose:
                print("Scale:", scale)
            self.scale = scale
            self.filtration_range = self.create_filtration_range(scale)
            for rng in list(generators):
                start = time.time()
                passes = self.perform_test(rng)
                end = time.time()
                # If the end of file is reached, then set the value to EOF.
                if passes < 0:
                    results_dict[rng.get_name()]['max_scale'] = 'EOF'
                elif verbose:
                    print('{}:{}/{}'.format(rng.get_name(), passes, self.runs))
                    print("Time elapsed:", end - start)
                # add this result to the output.
                results_dict[rng.get_name()]['results'].append('{}/{}'.format(passes, self.runs))
                if passes <= failure_threshold:
                    generators.remove(rng)
                    if verbose:
                        print("Generator removed.")
                else:
                    # record this as the new scale passed at.
                    results_dict[rng.get_name()]['max_scale'] = scale
        total_end = time.time()
        total_time = total_end - total_start
        if verbose:
            print("Done, total time:", total_time)
        # return to previous values.
        self.scale = original_scale
        self.filtration_range = self.create_filtration_range(self.scale)
        return results_dict
