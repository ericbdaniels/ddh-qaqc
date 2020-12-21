import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from app import app, db_connection
from utils.misc import run_query, load_table
from utils import plots


@app.callback(
    [Output("comp-len-select", "options"), Output("comp-len-select", "disabled")],
    Input("comp-var-select", "value"),
)
def populate_comp_len(comp_var):
    if comp_var is None:
        raise PreventUpdate
    qry_str = f'SELECT DISTINCT comp_length FROM composites WHERE var = "{comp_var}";'
    comp_lengths = run_query(db_connection, qry_str)
    return [{"label": str(i), "value": i} for i in comp_lengths], False


@app.callback(Output("view-comps-btn", "disabled"), Input("comp-len-select", "value"))
def enable_view_comps_btn(value):
    return False


def comps_var_query(conn):
    qry_str = "SELECT DISTINCT var from composites"
    composited_vars = run_query(conn, qry_str)
    return composited_vars


def get_summary_statistics(values: np.ndarray):
    return {
        "count": np.sum(np.isfinite(values)),
        "min": np.nanmin(values),
        "mean": np.nanmean(values),
        "median": np.nanmedian(values),
        "max": np.nanmax(values),
        "variance": np.nanvar(values),
    }


@app.callback(
    [Output("plots-container", "children"), Output("comps-select-modal", "is_open")],
    Input("view-comps-btn", "n_clicks"),
    [State("comp-var-select", "value"), State("comp-len-select", "value")],
)
def load_plots(n_clicks, comps_var, comp_lengths):
    if n_clicks is None or n_clicks == 0:
        raise PreventUpdate
    dist_fig = plots.figure()
    violin_fig = plots.figure()
    scatter_3d_fig = plots.figure_3d()
    summary_stats = {}
    for comp_len in comp_lengths:
        qry_str = f'SELECT * from composites WHERE var="{comps_var}" AND comp_length={comp_len}'
        data = pd.read_sql(qry_str, db_connection)
        name = f"Comps @ {comp_len}"
        hist = go.Histogram(x=data.value, name=name, legendgroup=name)
        cdf = plots.cdf(data.value.values, name=name, legendgroup=name)
        dist_fig.add_traces([hist, cdf])

        scatter_3d = go.Scatter3d(
            x=data.X,
            y=data.Y,
            z=data.Z,
            mode="markers",
            marker_color=data.value,
            name=name,
        )
        scatter_3d_fig.add_trace(scatter_3d)

        violin = go.Violin(x=data.values, name=name, side="positive")
        violin_fig.add_trace(violin)
        summary_stats[comp_len] = get_summary_statistics(data.value)
    plots_layout = [
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        figure=scatter_3d_fig,
                        className="mx-auto",
                        style={"height": "70vh"},
                    ),
                    width=6,
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            dbc.Col(
                                dcc.Graph(
                                    figure=dist_fig,
                                    className="mx-auto",
                                    style={"height": "45vh"},
                                )
                            )
                        ),
                        dbc.Row(
                            dbc.Col(
                                dcc.Graph(
                                    figure=violin_fig,
                                    className="mx-auto",
                                    style={"height": "45vh"},
                                )
                            )
                        ),
                    ],
                    width=6,
                ),
            ]
        ),
        dbc.Row(dbc.Col(load_table(pd.DataFrame.from_dict(summary_stats)))),
    ]
    return plots_layout, False


modal = dbc.Modal(
    id="comps-select-modal",
    children=[
        dbc.ModalHeader("Select Composites to View", className="p-2"),
        dbc.ModalBody(
            children=[
                dcc.Dropdown(
                    id="comp-var-select",
                    options=[
                        {"label": v, "value": v} for v in comps_var_query(db_connection)
                    ],
                ),
                dcc.Dropdown(
                    id="comp-len-select",
                    multi=True,
                    disabled=True,
                ),
                dbc.Button(
                    "View Data",
                    id="view-comps-btn",
                    color="primary",
                    className="mr-1",
                    disabled=True,
                ),
            ]
        ),
    ],
    size="lg",
    is_open=True,
    centered=True,
    autoFocus=True,
)

layout = dbc.Container([modal, dbc.Container(id="plots-container", fluid=True)])
