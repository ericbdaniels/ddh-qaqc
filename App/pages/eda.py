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
from itertools import cycle

COLORS = ["#0b5e76", "#043755", "#61616b", "#99c5b5", "#e5f4e3"]


@app.callback(
    [
        Output("comp-len-select", "options"),
        Output("comp-len-select", "value"),
        Output("comp-len-select", "disabled"),
    ],
    Input("comp-var-select", "value"),
)
def populate_comp_len(comp_var):
    if comp_var is None:
        raise PreventUpdate
    qry_str = f'SELECT DISTINCT comp_length FROM composites WHERE var = "{comp_var}";'
    comp_lengths = run_query(db_connection, qry_str)
    comp_lengths.sort()
    options = [{"label": str(i), "value": i} for i in comp_lengths] + [
        {"label": "raw assays", "value": "assay"}
    ]
    values = comp_lengths + ["assay"]
    return options, values, False


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
    dist_fig = plots.figure(
        layout_xaxis=dict(title="Value"),
        layout_yaxis=dict(title="F(x)"),
    )
    dist_fig.update_layout(
        yaxis2={
            "autorange": True,
            "title": "CDF",
            "side": "right",
            "zeroline": False,
            "overlaying": "y",
        }
    )
    violin_fig = plots.figure(layout_xaxis=dict(title="value"))
    scatter_3d_fig = plots.figure_3d()
    summary_stats = {}
    color_cycle = cycle(COLORS)
    for comp_len in comp_lengths:
        icolor = next(color_cycle)
        if comp_len == "assay":
            qry_str = f"SELECT X,Y,Z, {comps_var} from desurvey;"
            data = pd.read_sql(qry_str, db_connection)
            data.rename(columns={comps_var: "value"}, inplace=True)
            name = "Raw Assay"
        else:
            qry_str = f'SELECT * from composites WHERE var="{comps_var}" AND comp_length={comp_len}'
            data = pd.read_sql(qry_str, db_connection)
            name = f"Comps @ {comp_len}"
        hist = go.Histogram(
            x=data.value,
            name=name,
            legendgroup=name,
            marker_color=icolor,
            histnorm="probability density",
            opacity=0.9,
            nbinsx=20,
        )
        cdf = plots.cdf(
            data.value.values,
            name=name,
            legendgroup=name,
            yaxis="y2",
            showlegend=False,
            marker_color=icolor,
        )
        dist_fig.add_traces([hist, cdf])

        scatter_3d = go.Scatter3d(
            x=data.X,
            y=data.Y,
            z=data.Z,
            mode="markers",
            marker_color=data.value,
            marker_size=4,
            marker_colorscale="Viridis",
            name=name,
            marker_opacity=0.4,
        )
        scatter_3d_fig.add_trace(scatter_3d)

        violin = go.Violin(
            x=data.value,
            name=name,
            side="positive",
            width=3,
            fillcolor=icolor,
            line_color=icolor,
            opacity=0.5,
            points=False,
        )
        violin_fig.add_trace(violin)
        summary_stats[comp_len] = get_summary_statistics(data.value)
    stats_df = pd.DataFrame.from_dict(summary_stats, orient="index").round(4)
    stats_df.reset_index(inplace=True)
    stats_df.rename(columns={"index": "Comp. Length"}, inplace=True)
    plots_layout = [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            figure=scatter_3d_fig,
                            className="mx-auto",
                            style={"height": "60vh"},
                            config={"displaylogo": False},
                        ),
                        html.Div(
                            load_table(stats_df),
                            className="m-2",
                            style={"bottom": "5%", "width": "45%", "position": "fixed"},
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            figure=dist_fig,
                            className="mx-auto",
                            style={"height": "45vh"},
                            config={"displaylogo": False},
                        ),
                        dcc.Graph(
                            figure=violin_fig,
                            className="mx-auto",
                            style={"height": "45vh"},
                            config={"displaylogo": False},
                        ),
                    ],
                    width=6,
                ),
            ]
        ),
    ]
    return plots_layout, False


def data_select_modal(conn):
    modal = dbc.Modal(
        id="comps-select-modal",
        children=[
            dbc.ModalHeader("Select Composites to View", className="p-2"),
            dbc.ModalBody(
                children=[
                    dbc.Form(
                        [
                            dbc.FormGroup(
                                [
                                    dbc.Label("Composited Variable"),
                                    dcc.Dropdown(
                                        id="comp-var-select",
                                        options=[
                                            {"label": v, "value": v}
                                            for v in comps_var_query(conn)
                                        ],
                                        style={"padding": "5px"},
                                    ),
                                ]
                            ),
                            dbc.FormGroup(
                                [
                                    dbc.Label("Composite Length(s)"),
                                    dcc.Dropdown(
                                        id="comp-len-select",
                                        multi=True,
                                        disabled=True,
                                        style={"padding": "5px"},
                                    ),
                                ]
                            ),
                            dbc.Button(
                                "View Data",
                                id="view-comps-btn",
                                color="primary",
                                className="mr-1",
                                disabled=True,
                            ),
                        ]
                    )
                ]
            ),
        ],
        size="lg",
        is_open=True,
        centered=True,
        autoFocus=True,
    )
    return modal


def load_page(conn):
    return dbc.Container(
        [
            data_select_modal(conn),
            dcc.Loading(
                dbc.Container(id="plots-container", fluid=True),
                type="circle",
                style={"margin-top": "25%"},
            ),
        ],
        fluid=True,
        style={"padding": "10px"},
    )
