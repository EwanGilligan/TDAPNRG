import kmapper as km

from src.generator.FromBinaryFile import FromBinaryFile
from src.generator.Randu import Randu
from src.randology.HypercubeTest import HypercubeTest

rng = FromBinaryFile("TrueRandom1", 12000)
test = HypercubeTest(number_of_points=10000, reference_rng=rng)
datacloud = test.generate_points(Randu(1))
mapper = km.KeplerMapper(verbose=1)
projected_data = mapper.fit_transform(datacloud, projection=[0, 1])
graph = mapper.map(projected_data, datacloud, cover=km.Cover(n_cubes = 45))
mapper.visualize(graph, path_html="not_random.html")
