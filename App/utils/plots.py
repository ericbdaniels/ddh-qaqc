import plotly.graph_objs as go
import dash_core_components as dcc
import numpy as np


def trace_histogram(data, name):
    # TODO: refactor univaritate_eda and get rid of this
    f = go.Figure(layout_template="none")
    f.add_histogram(x=data, name=name)
    return f


def scatter(x, y, x_name, y_name, color=None, size=None):
    # TODO: refactor univaritate_eda and get rid of this

    f = go.Figure(
        layout_template="none", layout_xaxis_title=x_name, layout_yaxis_title=y_name
    )
    f.add_scatter(x=x, y=y, marker_color=color, marker_size=size, mode="markers")
    return f


def cdf(values: np.ndarray, **kwargs):
    quants = np.linspace(0.01, 0.99, 200)
    quant_values = np.quantile(values, quants)
    return go.Scatter(x=quant_values, y=quants, mode="lines", **kwargs)


def scatter3d(
    x,
    y,
    z,
    x_name="Easting",
    y_name="Northing",
    z_name="Elevation",
    color=None,
    size=3,
):
    # TODO: refactor univaritate_eda and get rid of this

    f = go.Figure(
        layout_template="none",
        layout_scene_aspectmode="data",
        layout_scene_xaxis_title=x_name,
        layout_scene_yaxis_title=y_name,
        layout_scene_zaxis_title=z_name,
    )
    f.add_scatter3d(x=x, y=y, z=z, marker_color=color, marker_size=size, mode="markers")
    return f


def figure(**kwargs):
    f = go.Figure(layout_template="none", **kwargs)
    return f


def figure_3d(**kwargs):
    f = go.Figure(
        layout_template="none",
        layout_scene_aspectmode="data",
        layout_scene_xaxis_title="EASTING",
        layout_scene_yaxis_title="NORTHING",
        layout_scene_zaxis_title="ELEVATION",
        **kwargs
    )
    return f
