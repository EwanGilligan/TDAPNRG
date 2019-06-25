import os
import sys
import time

import numpy as np
import matplotlib

from src.randology import *
from src.pnrg import *

rng = FromBinaryFile("../random-org-seq/TrueRandom1", 12000)
rng2 = FromBinaryFile("../random-org-seq/TrueRandom2", 12000)
python_rand = pythonRandom("Python Random")
gameRand = GameRand(0xDEADBEEF)
randu = Randu(int(time.time()))
test = HypercubeTest(runs=1, number_of_points=12000, dimension=3, homology_dimension=0, filtration_size=20,
                     reference_rng=rng, scale=1.0, max_filtration_value=0.1)
# test.visualise_failure(randu)
# start = time.time()
# print(test.perform_test(randu))
# end = time.time()
# print("Time elapsed:", end - start)
x = test.generate_points(randu)
result = ripser(x, thresh=0.2, do_cocycles=True)
cocycles = result['cocycles']
diagrams = result['dgms']
dgm1 = diagrams[1]
idx = np.argmax(dgm1[:, 1] - dgm1[:, 0])
cocycle_points_array = []
last300 = cocycles[1][-300:]
for cocycle in cocycles[1]:
    #print(cocycle)
    indices = np.unique(np.concatenate((np.take(cocycle, 0, axis=1), np.take(cocycle, 1, axis=1))))
    cocycle_points = np.array([x[i] for i in indices])
    cocycle_points_array.append(cocycle_points)
plot_3d(cocycle_points_array)
plt.show()

# test.test_directory("../pseudo-random-sequences")
