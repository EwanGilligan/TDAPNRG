
import kmapper as km
from sklearn import cluster
import numpy as np


def visualise_point_cloud(point_cloud : np.ndarray, epsilon : float, n_cubes : int, filename):
    mapper = km.KeplerMapper(verbose=1)
    nerve = km.GraphNerve(10)
    projection = list(range(point_cloud.shape[1]))
    projected_data = mapper.fit_transform(point_cloud, projection=projection)
    clusterer = cluster.DBSCAN(eps=epsilon)
    graph = mapper.map(projected_data, point_cloud, cover=km.Cover(n_cubes=n_cubes), nerve=nerve, clusterer=clusterer)
    mapper.visualize(graph, path_html=filename)
