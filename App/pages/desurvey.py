import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from app import app, db_connection
from dash.exceptions import PreventUpdate
from utils.desurvey import desurvey

readme_text = dbc.Container(
    [
        dcc.Markdown("# Desurveying"),
        html.Hr(),
        dcc.Markdown(
            """
            ## Two Options for Interpolation:
            1. Simple Tanget 
            2. Minimum Curvature

            Seequent provides a nice summary [here](https://www.seequent.com/the-dark-art-of-drillhole-desurveying/).

    """
        ),
    ]
)

form = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.Label("Desurvey Method: ")),
                dbc.Col(
                    dcc.Dropdown(
                        id="desurvey-dropdown",
                        options=[
                            {"label": "Minimum Curvature", "value": "mincurve"},
                            {"label": "Simple Tangent", "value": "tangent"},
                        ],
                        value="mincurve",
                    )
                ),
                dbc.Col(
                    dbc.Button(
                        "Submit",
                        id="desurvey-submit-btn",
                        color="primary",
                        className="mr-1",
                    ),
                ),
            ]
        )
    ]
)

content = dbc.Container([readme_text, form, html.Div(id="desurvey-output")])


@app.callback(
    Output("desurvey-output", "children"),
    Input("desurvey-submit-btn", "n_clicks"),
    State("desurvey-dropdown", "value"),
)
def calc_desurvey(n_clicks, value):
    if n_clicks is not None:
        survey = pd.read_sql("SELECT * from  survey", db_connection)
        collar = pd.read_sql("SELECT * from collar", db_connection)
        desurvey_df = desurvey(survey, collar, value)
        desurvey_df.to_sql("desurvey", db_connection)
        return "Desurvey Complete!"
    else:
        raise PreventUpdate
