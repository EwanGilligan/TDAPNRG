import kmapper as km
from sklearn import cluster
import numpy as np
from ripser import ripser
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly
import plotly.graph_objs as go


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


def plot_3d_interactive(point_clouds, title):
    assert len(point_clouds) > 0, "Plot data is empty"
    data = []
    for point_cloud in point_clouds:
        xs = np.take(point_cloud, 0, axis=1)
        ys = np.take(point_cloud, 1, axis=1)
        zs = np.take(point_cloud, 2, axis=1)
        data.append(go.Scatter3d(x=xs.tolist(),
                                 y=ys.tolist(),
                                 z=zs.tolist(),
                                 mode='markers',
                                 marker=dict(
                                     size=2,
                                 )
                                 )
                    )
    plotly.offline.plot({
        "data": data,
        "layout": go.Layout(title=title),
    }, filename=title + ".html")


def plot_connected_components(x, title):
    result = ripser(x, thresh=0.1, do_cocycles=True)
    cocycles = result['cocycles']
    diagrams = result['dgms']
    dgm1 = diagrams[1]
    # large_cocyles = filter(lambda c: len(c) > x.shape[0] / 15, cocycles[1])
    idx = np.argmax([len(x) for x in cocycles[1]])
    large_cocyles = [cocycles[1][idx]]
    # idx = np.argmax(dgm1[:, 1] - dgm1[:, 0])
    # cocycle = cocycles[1][idx]
    # D = result['dperm2all']
    # thresh = dgm1[idx, 1]
    point_clouds = []
    for cocycle in large_cocyles:
        column1 = np.take(cocycle, 0, axis=1)
        column2 = np.take(cocycle, 1, axis=1)
        indices = np.unique(np.concatenate((column1, column2)))
        cocycle_points = np.array([x[i] for i in indices])
        point_clouds.append(cocycle_points)
    plot_3d_interactive(point_clouds, title)
