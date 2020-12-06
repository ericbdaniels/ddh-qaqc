import plotly.graph_objs as go
import dash_core_components as dcc


def histogram(data, name):
    f = go.Figure(layout_template="none")
    f.add_histogram(x=data, name=name)
    return f


def scatter(x, y, x_name, y_name, color=None, size=None):
    f = go.Figure(
        layout_template="none", layout_xaxis_title=x_name, layout_yaxis_title=y_name
    )
    f.add_scatter(x=x, y=y, marker_color=color, marker_size=size, mode="markers")
    return f


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
    f = go.Figure(
        layout_template="none",
        layout_scene_aspectmode="data",
        layout_scene_xaxis_title=x_name,
        layout_scene_yaxis_title=y_name,
        layout_scene_zaxis_title=z_name,
    )
    f.add_scatter3d(x=x, y=y, z=z, marker_color=color, marker_size=size, mode="markers")
    return f