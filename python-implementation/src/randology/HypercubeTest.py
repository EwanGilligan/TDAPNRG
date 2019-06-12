import dionysus as d
import numpy as np
from scipy import stats
from ripser import Rips
from typing import List
from matplotlib import pyplot

from src.generator import RNG


def create_filtration_range(n=20, max_value=0.1):
    return np.linspace(0, max_value, n)


class HypercubeTest:

    def __init__(self, reference_rng: RNG, number_of_points: int, runs: int = 10, dimension: int = 3,
                 max_simplex_dim: int = 1,
                 filtration_size: int = 20, max_filtration_value: int = 0.1) -> None:
        self.runs = runs
        self.number_of_points = number_of_points
        self.dimension = dimension
        self.max_simplex_dim = max_simplex_dim
        # self.filtration_range = np.array([0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.070, 0.075, 0.08, 0.085, 0.09, 0.095])
        # self.filtration_size = len(self.filtration_range)
        self.filtration_range = create_filtration_range(filtration_size, max_filtration_value)
        self.filtration_size = filtration_size
        self.reference_distribution = self.generate_distribution(reference_rng)

    def generate_distribution(self, rng: RNG):
        points = self.generate_points(rng)
        diagrams = self.generate_diagram(points)
        homology = self.generate_homology(diagrams)
        return homology[0]

    def generate_diagram(self, points: np.array) -> List[np.ndarray]:
        filtration = Rips(maxdim=self.max_simplex_dim, thresh=self.filtration_range[-1], verbose=False)
        diagrams = filtration.fit_transform(points)
        return diagrams

    def generate_points(self, rng: RNG) -> np.array:
        return np.array([[rng.next_float() for _ in range(self.dimension)] for _ in range(self.number_of_points)])

    def generate_homology(self, diagrams):
        homology = {dimension: np.zeros(self.filtration_size) for dimension in range(self.max_simplex_dim + 1)}
        for dimension, diagram, in enumerate(diagrams):
            if dimension <= self.max_simplex_dim and len(diagram) > 0:
                homology[dimension] = np.array(
                    [np.array(((self.filtration_range >= point[0]) & (self.filtration_range <= point[1])).astype(int))
                     for point
                     in diagram]).sum(axis=0).tolist()
        return homology

    def single_run(self, rng: RNG):
        observed_distribution = self.generate_distribution(rng)
        print(observed_distribution)
        print(self.reference_distribution)
        return stats.chisquare(f_obs=observed_distribution, f_exp=self.reference_distribution)[1]

    def perform_test(self, rng: RNG):
        passes = 0
        for i in range(self.runs):
            if self.single_run(rng) > 0.01:
                passes += 1
        return passes
