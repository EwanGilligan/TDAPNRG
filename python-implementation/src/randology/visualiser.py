import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly
import plotly.graph_objs as go
import pyximport

pyximport.install()
from .vrips import one_skeleton


def plot_3d(point_cloud_array):
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(111, projection='3d')
    print(len(point_cloud_array))
    for point_cloud in point_cloud_array:
        xs = np.take(point_cloud, [0], axis=1)
        ys = np.take(point_cloud, [1], axis=1)
        zs = np.take(point_cloud, [2], axis=1)
        ax.scatter(xs, ys, zs, '.', s=1)


def plot_3d_interactive(point_clouds, title) -> None:
    """
    Create an interactive plot of the point clouds supplied.

    :param point_clouds: Iterable containing point clouds.
    :param title: Title of the plot.
    """
    assert len(point_clouds) > 0, "Plot data is empty"
    data = []
    for point_cloud in point_clouds:
        xs = point_cloud[:, 0]  # np.take(point_cloud, 0, axis=1)
        ys = point_cloud[:, 1]  # np.take(point_cloud, 1, axis=1)
        zs = point_cloud[:, 2]  # np.take(point_cloud, 2, axis=1)
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


def visualise_connected_components_animated(point_cloud, title, filepath, filtration_range):
    threshhold = filtration_range[-1]
    # f = d.fill_rips(point_cloud, 1, threshhold)
    # f.sort()
    f = one_skeleton(point_cloud, threshhold)
    f.sort(key=lambda x: x[1])
    filtration_iter = iter(filtration_range)
    # So the 0 value will be grouped.
    prev_filtration_val = -1
    filtration_val = next(filtration_iter)
    filtrations_grouping = []
    filtration_list = []
    for s in f:
        if not (prev_filtration_val < s[1] <= filtration_val):
            prev_filtration_val = filtration_val
            filtration_val = next(filtration_iter)
            filtrations_grouping.append(filtration_list)
            filtration_list = []
        # Don't add 0-simplices, as these will just be all the values in the point cloud.
        # if s.dimension() != 0:
        filtration_list.append(s)
    filtrations_grouping.append(filtration_list)
    plot_connected_components(point_cloud, filtrations_grouping, title, filepath, filtration_range)


def plot_connected_components(point_cloud, filtrations, title, filepath, filtration_range):
    """

    :param point_cloud: Numpy array on 3 dimensional points in Euclidean space.
    :param filtrations: List of lists that contains simplices (edge chains), that are grouped based on their value and the filtration range.
    :param title: Title for the plot
    :param filepath: filepath for the plot.
    :param filtration_range: array of various distances to use as ranges when splitting up the simplices being added.
    """
    threshold = filtration_range[-1]
    figure = {
        'data': [],
        'layout': {},
        'frames': [],
    }
    figure['layout']['title'] = title
    figure['layout']['showlegend'] = False
    figure['layout']['scene'] = dict(xaxis=dict(range=[0, 1]),
                                     yaxis=dict(range=[0, 1]),
                                     zaxis=dict(range=[0, 1])
                                     )
    figure['layout']['hovermode'] = 'closest'
    figure['layout']['updatemenus'] = [{
        'buttons': [
            {'args': [None, {'frame': {'duration': 1000, 'redraw': True},
                             'fromcurrent': True,  # 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}
                             }],
             'label': 'Play',
             'method': 'animate'},
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                                  'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }]
    figure['layout']['sliders'] = {
        'args': [
            'transition', {
                'duration': 400,
            }
        ],
        'initialValue': '0',
        'plotlycommand': 'animate',
        'values': filtration_range,
        'visible': True
    }
    sliders_dict = {
        'active': 0,
        'yanchor': 'top',
        'xanchor': 'left',
        'currentvalue': {
            'font': {'size': 20},
            'prefix': 'Epsilon:',
            'visible': True,
            'xanchor': 'right'
        },
        'pad': {'b': 10, 't': 50},
        'len': 0.9,
        'x': 0.1,
        'y': 0,
        'steps': []
    }
    # make data trace
    xn = point_cloud[:, 0]
    yn = point_cloud[:, 1]
    zn = point_cloud[:, 2]
    # point trace always displayed.
    point_trace = go.Scatter3d(x=xn,
                               y=yn,
                               z=zn,
                               mode='markers',
                               marker=dict(symbol='circle',
                                           size=1,
                                           color='black'),
                               name="Point cloud")
    figure['data'].append(point_trace)
    # data figure to use for edges.
    figure['data'].append(go.Scatter3d(x=[None], y=[None], z=[None]))
    # make frames:
    i = 0
    # frame_data = [point_trace]
    xe = [None]
    ye = [None]
    ze = [None]
    insertion_values = [threshold]
    for filtration in filtrations:
        frame = {'data': None, 'name': i}
        # Only the individual nodes will be added at 0, so no lines are needed.
        if filtration_range[i] > 0:
            # xe = []
            # ye = []
            # ze = []
            for simplex in filtration:
                for v in simplex[0]:
                    xe.append(point_cloud[v][0])
                    ye.append(point_cloud[v][1])
                    ze.append(point_cloud[v][2])
                    insertion_values.append(simplex[1])
                # add None to break the line.
                xe.append(None)
                ye.append(None)
                ze.append(None)
                # threshold to used here to set the maximum value of the scale
                insertion_values.append(threshold)
        edge_trace = go.Scatter3d(x=xe,
                                  y=ye,
                                  z=ze,
                                  mode='lines',  # +markers',
                                  line=dict(color=insertion_values,
                                            colorscale='Viridis',
                                            showscale=True),
                                  # marker=dict(symbol='circle',
                                  #             size=1,
                                  #             color='black')
                                  )
        # frame_data.append(edge_trace)
        # frame_data.insert(0, edge_trace)
        # add all data from previous frames.
        frame['data'] = [edge_trace]  # frame_data.copy()
        # update edge trace.
        frame['traces'] = [1]  # [i + 1]
        figure['frames'].append(frame)
        slider_step = {'args': [
            [i],
            {'frame': {'duration': 1000, 'redraw': True},
             'mode': 'immediate',
             'transition': {'duration': 0}}
        ],
            'label': '{:.3}'.format(filtration_range[i]),
            'method': 'animate'}
        sliders_dict['steps'].append(slider_step)
        i += 1
    figure['layout']['sliders'] = [sliders_dict]
    plotly.offline.plot(figure, filename=filepath + title + ".html", auto_play=False, auto_open=False)
