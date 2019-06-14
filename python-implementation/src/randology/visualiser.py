import time

import kmapper as km
from sklearn import cluster

from src.generator.FromBinaryFile import FromBinaryFile
from src.generator.GameRand import GameRand
from src.generator.Randu import Randu
from src.randology.HypercubeTest import HypercubeTest, generate_points
from matplotlib import pyplot

rng = Randu(int(time.time()))
#rng = FromBinaryFile("TrueRandom1", 12000)
#rng = GameRand(int(time.time()))
datacloud = generate_points(rng, 3, 10000)
mapper = km.KeplerMapper(verbose=1)
nerve = km.GraphNerve(10)
projected_data = mapper.fit_transform(datacloud, projection=[0, 1, 2])
clusterer = cluster.DBSCAN(eps=0.05)
graph = mapper.map(projected_data, datacloud, cover=km.Cover(n_cubes=8), nerve=nerve, clusterer=clusterer)
mapper.visualize(graph, path_html=rng.get_name() + ".html")
