import dionysus as d
import numpy as np
from scipy import stats
import gudhi

from src.generator import RNG


class HypercubeTest:

    def __init__(self, runs: int, number_of_points: int, dimension: int) -> None:
        self.runs = runs
        self.number_of_points = number_of_points
        self.dimension = dimension

    def generate_diagram(self, rng: RNG) -> d.Diagram:
        # generate the point cloud.
        points = np.array([[rng.next_float() for i in range(self.dimension)] for i in range(self.number_of_points)])
        filtration = d.fill_rips(points, 1, 0.1)
        homology_groups = d.homology_persistence(filtration)
        diagram = d.init_diagrams(homology_groups, filtration)
        return diagram

    def single_run(self, rng: RNG, reference_diagram: d.Diagram) -> float:
        diagram = self.generate_diagram(rng)
        return d.bottleneck_distance(diagram, reference_diagram)

