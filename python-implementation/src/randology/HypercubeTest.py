import dionysus as d
import numpy as np
from scipy import stats
from ripser import Rips
from typing import List
from matplotlib import pyplot

from src.generator import RNG

def create_filtration_range(n=100, max_value=1.0):
    return np.linspace(0, max_value, n)


class HypercubeTest:

    def __init__(self, runs: int, number_of_points: int, dimension: int, max_simplex_dim: int) -> None:
        self.runs = runs
        self.number_of_points = number_of_points
        self.dimension = dimension
        self.max_simplex_dim = max_simplex_dim
        self.filtration_size = 10

    def single_run(self, rng: RNG, reference_diagram: d.Diagram):
        points = self.generate_points(rng)
        filtration_range = create_filtration_range(self.filtration_size, 0.1)
        diagrams = self.generate_diagram(points)
        homology = {dimension : np.zeros(self.filtration_size) for dimension in range(self.max_simplex_dim + 1)}
        print(diagrams)
        for dimension, diagram, in enumerate(diagrams):
            if dimension <= self.max_simplex_dim and len(diagram) > 0:
                homology[dimension] = np.array([np.array(((filtration_range >= point[0]) & (filtration_range <= point[1])).astype(int)) for point in diagram]).sum(axis=0).tolist()
        print(homology)

    def generate_diagram(self, points: np.array) -> List[np.ndarray]:
        filtration = Rips(maxdim=self.max_simplex_dim)
        diagrams = filtration.fit_transform(points)
        return diagrams

    def generate_points(self, rng: RNG) -> np.array:
        return np.array([[rng.next_float() for _ in range(self.dimension)] for _ in range(self.number_of_points)])
