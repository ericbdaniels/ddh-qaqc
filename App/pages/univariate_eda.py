from itertools import cycle
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from app import app, db_connection
from dash.exceptions import PreventUpdate
from utils import plots, misc

COLORS = ["#721817", "#fa9f42", "#2b4162", "#0b6e4f", "#e0e0e2"]


def load_text():
    return dbc.Row(
        [
            dcc.Markdown("# Exploratory Data Analysis: Univariate"),
            html.Hr(),
        ]
    )


def stats_card(title, value, color):
    return dbc.Card(
        [
            dbc.CardBody(
                [html.H3(title, style={"color": color}), html.H2(f"{value:.3f}")]
            )
        ]
    )


def load_stats_cards(values):
    color_cycle = cycle(COLORS)
    stats_dict = {
        "Count": values.size,
        "Minimum": values.min(),
        "Median": values.median(),
        "Mean": values.mean(),
        "Maximum": values.max(),
        "Variance": values.var(),
    }
    return dbc.Row(
        [dbc.Col(stats_card(k, v, next(color_cycle))) for k, v in stats_dict.items()]
    )


def load_plots_content(x, y, z, values, lengths):
    plots_content = dbc.Row(
        [
            dbc.Col(
                dcc.Graph(
                    figure=plots.scatter3d(x, y, z, color=values),
                    className="mx-auto",
                    style={"height": "70vh"},
                ),
                width=8,
            ),
            dbc.Col(
                [
                    dbc.Row(
                        dcc.Graph(
                            figure=plots.scatter(
                                x=lengths,
                                x_name="Composite Length",
                                y=values,
                                y_name="Value",
                            ),
                        )
                    ),
                    dbc.Row(
                        dcc.Graph(
                            figure=plots.histogram(values, "Value"),
                        )
                    ),
                ],
                width=4,
            ),
        ]
    )
    return plots_content


def load_content(conn):
    assay_df = pd.read_sql("SELECT * from  desurveyed_assay", conn)
    text_row = load_text()
    stats_row = load_stats_cards(assay_df.Au)
    plots_row = load_plots_content(
        assay_df.X, assay_df.Y, assay_df.Z, assay_df.Au, assay_df._len
    )
    table = table = misc.load_table(assay_df)

    return dbc.Container([text_row, stats_row, plots_row, table], fluid=True)