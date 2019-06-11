import os
import sys

import gudhi
import numpy as np
import matplotlib

from src.generator.FromBinaryFile import FromBinaryFile
from src.generator.Randu import Randu
from src.randology.HypercubeTest import HypercubeTest
rng = FromBinaryFile("TrueRandom1", 40)
points = np.array([[rng.next_float() for i in range(4)] for i in range(10)])
print(points)
