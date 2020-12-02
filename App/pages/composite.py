import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from app import app, db_connection
from dash.exceptions import PreventUpdate
from utils.composite import composite_dh

readme_text = dbc.Container(
    [
        dcc.Markdown("# Compositing"),
        html.Hr(),
        dcc.Markdown(
            """
            ## Continuous Variables
            A simple mean compositing methodology is applied here. This is intended for continuous, linearly averaging variables.

    """
        ),
    ]
)


def generate_var_select_form(assay_column_names):
    select_form = dbc.FormGroup(
        [
            dbc.Label("Variable to Composite"),
            dcc.Dropdown(
                id="comp-var-select-dropdown",
                options=[{"label": name, "value": name} for name in assay_column_names],
            ),
        ]
    )
    return select_form


comp_len_form = dbc.FormGroup(
    [
        dbc.Label("Composite Length"),
        dbc.Input(type="number", min=0, value=5),
        dbc.Label("Minimum Interval"),
        dbc.Input(type="number", value=-1),
        dbc.FormText(
            "minimum interval size to consider in composite. -1 Implies no minimum"
        ),
    ]
)


def generate_comp_input_form(assay_column_names):
    input_form = dbc.Form(
        [
            generate_var_select_form(assay_column_names),
            comp_len_form,
            dbc.Button("Submit", id="comps-btn", className="mr-1"),
        ]
    )
    return input_form


def load_content(conn):
    cursor = conn.cursor()
    query = cursor.execute("PRAGMA table_info(assay);")
    query_results = query.fetchall()
    assay_column_names = [i[1] for i in query_results]
    content = dbc.Container(
        [
            readme_text,
            generate_comp_input_form(assay_column_names),
            html.Div(id="comp-output"),
        ]
    )
    return content