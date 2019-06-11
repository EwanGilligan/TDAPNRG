import dionysus as d
import numpy as np
from scipy import stats
from ripser import Rips
from typing import List
from matplotlib import pyplot

from src.generator import RNG


class HypercubeTest:

    def __init__(self, runs: int, number_of_points: int, dimension: int, max_simplex_dim: int) -> None:
        self.runs = runs
        self.number_of_points = number_of_points
        self.dimension = dimension
        self.max_simplex_dim = max_simplex_dim

    def single_run(self, rng: RNG, reference_diagram: d.Diagram):
        points = self.generate_points(rng)
        diagram = self.generate_diagram(points)

    def generate_diagram(self, points: np.array) -> List[np.ndarray]:
        filtration = Rips(maxdim=self.max_simplex_dim)
        diagrams = filtration.fit_transform(points)
        return diagrams

    def generate_points(self, rng: RNG) -> np.array:
        return np.array([[rng.next_float() for _ in range(self.dimension)] for _ in range(self.number_of_points)])
