import os
import sys
import time

import numpy as np
import matplotlib

from src.randology import *
from src.pnrg import *

rng = FromBinaryFile("../../random-org-seq/TrueRandom1", 12000)
rng2 = FromBinaryFile("../../random-org-seq/TrueRandom2", 12000)
fileRand = FromBinaryFile("../../pseudo-random-sequences/outGlibc48", 12000)
python_rand = pythonRandom("Python Random")
gameRand = GameRand(0xDEADBEEF)
randu = Randu(1)
lsfr = LFSR(0xDEADBEEF)
glibc48 = Glibc(0x2197B942509FF4DB)
test = HypercubeTest(runs=10, number_of_points=12000, dimension=3, homology_dimension=0, filtration_size=20,
                     reference_rng=rng2, scale=0.15)
start = time.time()
print(test.perform_test(glibc48))
end = time.time()
print("Time elapsed:", end - start)
# x = generate_points(glibc48, 12000, 3)
# #plot_3d_interactive([x], "Glibc")
# # # x2 = generate_points(randu, 12000, 3, 1)
# plot_connected_components(x, glibc48.get_name(), "../../visualisations/", 20)
# plot_connected_components(x2, randu.get_name(), "../../visualisations/", 20)


# test.test_directory("../pseudo-random-sequences")
