import dionysus as d
import numpy as np
import plotly
import plotly.graph_objs as go
from itertools import cycle
from cechmate.filtrations import Rips

# Distinct colours to use for plotting.
kelly_colors = ['#F2F3F4', '#222222', '#F3C300', '#875692', '#F38400', '#A1CAF1', '#BE0032', '#C2B280', '#848482',
                '#008856', '#E68FAC', '#0067A5', '#F99379', '#604E97', '#F6A600', '#B3446C', '#DCD300', '#882D17',
                '#8DB600', '#654522', '#E25822', '#2B3D26'][1:]  # skip white


def visualise_connected_components_animated_d(point_cloud, threshhold, title, filepath, filtration_range):
    f = d.fill_rips(point_cloud, 1, threshhold)
    f.sort()
    filtration_iter = iter(filtration_range)
    #So the 0 value will be grouped.
    prev_filtration_val = -1
    filtration_val = next(filtration_iter)
    filtrations_grouping = []
    filtration_list = []
    for s in f:
        if not (prev_filtration_val < s.data <= filtration_val):
            prev_filtration_val = filtration_val
            filtration_val = next(filtration_iter)
            filtrations_grouping.append(filtration_list)
            filtration_list = []
        # Don't add 0-simplices, as these will just be all the values in the point cloud.
        #if s.dimension() != 0:
        filtration_list.append(s)
    filtrations_grouping.append(filtration_list)
    wip_plot(point_cloud, filtrations_grouping, title, filepath, filtration_range)


def wip_plot(point_cloud, filtrations, title, filepath, filtration_range):
    """

    :param point_cloud: Numpy array on 3 dimensional points in Euclidean space.
    :param filtrations: List of lists that contains simplices (edge chains), that are grouped based on their value and the filtration range.
    :param title: Title for the plot
    :param filepath: filepath for the plot.
    :param filtration_range: array of various distances to use as ranges when splitting up the simplices being added.
    """
    figure = {
        'data': [],
        'layout': {},
        'frames': []
    }
    figure['layout']['title'] = title
    figure['layout']['scene'] = dict(xaxis=dict(range=[0, 1]),
                                     yaxis=dict(range=[0, 1]),
                                     zaxis=dict(range=[0, 1])
                                     )
    figure['layout']['hovermode'] = 'closest'
    figure['layout']['updatemenus'] = [{
        'buttons': [
            {'args': [None, {'frame': {'duration': 500, 'redraw': True},
                             'fromcurrent': True,  # 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}
                             }],
             'label': 'Play',
             'method': 'animate'}
        ],
        'pad': {'r': 10, 't': 87},
        'showactive': True,
        'type': 'buttons'
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
    colour_iter = cycle(kelly_colors)
    # point trace always displayed.
    point_trace = go.Scatter3d(x=xn,
                               y=yn,
                               z=zn,
                               mode='markers',
                               marker=dict(symbol='circle',
                                           size=1,
                                           color=next(colour_iter)),
                               name="Point cloud")
    figure['data'].append(point_trace)
    figure['data'] += [go.Scatter3d(x=[], y=[], z=[]) for _ in range(len(filtration_range))]
    # make frames:
    i = 0
    #frame_data = [point_trace]
    for filtration in filtrations:
        frame = {'data': None, 'name': str(filtration_range[i])}
        # Only the individual nodes will be added at 0, so no lines are needed.
        #if filtration_range[i] > 0:
        xe = []
        ye = []
        ze = []
        insertion_values = []
        for simplex in filtration:
            for v in simplex:
                xe.append(point_cloud[v][0])
                ye.append(point_cloud[v][1])
                ze.append(point_cloud[v][2])
            # add None to break the line.
            xe.append(None)
            ye.append(None)
            ze.append(None)
            insertion_values.append(str(simplex.data))
        edge_trace = go.Scatter3d(x=xe,
                                  y=ye,
                                  z=ze,
                                  mode='lines',
                                  line=dict(color=next(colour_iter)), )
            #frame_data.append(edge_trace)
            #frame_data.insert(0, edge_trace)
        # add all data from previous frames.
        frame['data'] = [edge_trace]#frame_data.copy()
        frame['traces'] = [i + 1]
        figure['frames'].append(frame)
        slider_step = {'args': [
            [filtration_range[i]],
            {'frame': {'duration': 300, 'redraw': True},
             'mode': 'immediate',
             'transition': {'duration': 300}}
        ],
            'label': filtration_range[i],
            'method': 'animate'}
        sliders_dict['steps'].append(slider_step)
        i += 1
    figure['layout']['sliders'] = [sliders_dict]
    plotly.offline.plot(figure, filename=filepath + title + ".html")


def plot_connected_components_animated_d(x, filtrations, title, filepath, filtration_range):
    xn = x[:, 0]
    yn = x[:, 1]
    zn = x[:, 2]
    colour_iter = cycle(kelly_colors)
    # point trace always displayed.
    point_trace = go.Scatter3d(x=xn,
                               y=yn,
                               z=zn,
                               mode='markers',
                               marker=dict(symbol='circle',
                                           size=1,
                                           color='black'))
    data = []  # [point_trace]
    frames = []
    for filtration in filtrations:
        xe = []
        ye = []
        ze = []
        for simplex in filtration:
            for v in simplex:
                xe.append(x[v][0])
                ye.append(x[v][1])
                ze.append(x[v][2])
            xe.append(None)
            ye.append(None)
            ze.append(None)
        edge_trace = go.Scatter3d(x=xe,
                                  y=ye,
                                  z=ze,
                                  mode='lines',
                                  line=dict(color=next(colour_iter)))
        data.append(edge_trace)
        frames.append(dict(data=data.copy()))

    layout = go.Layout(title=title,
                       # scene=dict(
                       #     xaxis=dict(nticks=4, range=[0, 1], autorange=False),
                       #     yaxis=dict(nticks=4, range=[0, 1], autorange=False),
                       #     zaxis=dict(nticks=4, range=[0, 1], autorange=False),
                       # ),
                       # width=1000,
                       # margin=dict(
                       #     r=20, l=10,
                       #     b=10, t=10),
                       updatemenus=[{
                           'buttons': [
                               {'args': [None],
                                'label': 'Play',
                                'method': 'animate'}
                           ],
                           'pad': {'r': 10, 't': 87},
                           'showactive': False,
                           'type': 'buttons'
                       }]
                       )
    plotly.offline.plot({
        "data": [point_trace],
        "frames": frames,
        "layout": layout

    }, filename=filepath + title + ".html", auto_play=False)
