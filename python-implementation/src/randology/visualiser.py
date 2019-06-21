import kmapper as km
from sklearn import cluster
import numpy as np
from ripser import ripser
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def visualise_point_cloud(point_cloud: np.ndarray, epsilon: float, n_cubes: int, filename):
    mapper = km.KeplerMapper(verbose=1)
    nerve = km.GraphNerve(10)
    projection = list(range(point_cloud.shape[1]))
    projected_data = mapper.fit_transform(point_cloud, projection=projection)
    clusterer = cluster.DBSCAN(eps=epsilon)
    graph = mapper.map(projected_data, point_cloud, cover=km.Cover(n_cubes=n_cubes), nerve=nerve, clusterer=clusterer)
    mapper.visualize(graph, path_html=filename)


def draw_line_coloured(x, c):
    for i in range(x.shape[0] - 1):
        plt.plot(x[i:i + 2, 0], x[i:i + 2, 1], c=c[i, :], lineWidth=3)


def plot_cocycle_2d(d, x, cocycle, thresh):
    """
    Given a 2D point cloud x, display a cocycle projected
    onto edges under a given threshold "thresh"
    """
    # Plot all edges under the threshold
    n = x.shape[0]
    t = np.linspace(0, 1, 10)
    c = plt.get_cmap('Greys')
    c = c(np.array(np.round(np.linspace(0, 255, len(t))), dtype=np.int32))
    c = c[:, 0:3]

    for i in range(n):
        for j in range(n):
            if d[i, j] <= thresh:
                Y = np.zeros((len(t), 2))
                Y[:, 0] = x[i, 0] + t * (x[j, 0] - x[i, 0])
                Y[:, 1] = x[i, 1] + t * (x[j, 1] - x[i, 1])
                draw_line_coloured(Y, c)
    # Plot cocycle projected to edges under the chosen threshold
    for k in range(cocycle.shape[0]):
        [i, j, val] = cocycle[k, :]
        if d[i, j] <= thresh:
            [i, j] = [min(i, j), max(i, j)]
            a = 0.5 * (x[i, :] + x[j, :])
            plt.text(a[0], a[1], '%g' % val, color='b')
    # Plot vertex labels
    for i in range(n):
        plt.text(x[i, 0], x[i, 1], '%i' % i, color='r')
    plt.axis('equal')


def plot_3d(point_cloud_array):
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(111, projection='3d')
    print(len(point_cloud_array))
    for point_cloud in point_cloud_array:
        xs = np.take(point_cloud, [0], axis=1)
        ys = np.take(point_cloud, [1], axis=1)
        zs = np.take(point_cloud, [2], axis=1)
        ax.scatter(xs, ys, zs, '.', s=1)
