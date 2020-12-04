import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, MATCH
from dash.exceptions import PreventUpdate
import pandas as pd
import base64
import io
import json
from app import app, db_connection
from utils.desurvey import desurvey_assay


def parse_data(content, filename):
    content_string = content.split(".")[1].split(",")[-1]
    decoded = base64.b64decode(content_string)
    if "csv" in filename:
        return pd.read_csv(io.StringIO(decoded.decode("utf-8")))
    elif "xls" in filename:
        return pd.read_excel(io.BytesIO(decoded))
    else:
        return None


@app.callback(
    Output({"type": "upload-output", "name": MATCH}, "children"),
    [
        Input({"type": "upload", "name": MATCH}, "contents"),
        Input({"type": "upload", "name": MATCH}, "filename"),
    ],
)
def load_data_from_csv(content, filename):
    if filename is None:
        raise PreventUpdate
    else:
        table_name = json.loads(
            dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        )["name"]
        df = parse_data(content, filename)
        df.to_sql(table_name, db_connection)
        return f"{filename} Loaded!"


def create_uploader(id_name):
    uploader = dcc.Upload(
        id={"type": "upload", "name": id_name},
        children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
        className="mx-auto",
        style={
            "width": "90%",
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px",
        },
    )
    return uploader


def tab_content(name):
    return dbc.Card(
        [
            html.P(f"Select {name} data for Upload (commonly {name}.csv)"),
            create_uploader(name),
            html.Div(id={"type": "upload-output", "name": name}),
        ]
    )


modal = dbc.Modal(
    [
        dbc.ModalHeader("Select Files For Upload", className="p-2"),
        dbc.ModalBody(
            children=[
                dbc.Tabs(
                    [
                        dbc.Tab(tab_content("assay"), label="Assay"),
                        dbc.Tab(tab_content("collar"), label="Collar"),
                        dbc.Tab(tab_content("survey"), label="Survey"),
                    ]
                ),
                dbc.Button(
                    "Desurvey Assays",
                    id="desurvey-assay-btn",
                    color="primary",
                    className="mr-1",
                ),
                html.Div(id="desurvey-assay-output"),
            ]
        ),
    ],
    size="lg",
    is_open=True,
    centered=True,
    autoFocus=True,
)


@app.callback(
    Output("desurvey-assay-output", "children"), Input("desurvey-assay-btn", "n_clicks")
)
def desurvey_raw_assays(n_clicks):
    if n_clicks is not None:
        assay = pd.read_sql("SELECT * from  assay", db_connection)
        assay["midpt"] = (assay.FROM + assay.TO) / 2
        survey = pd.read_sql("SELECT * from  survey", db_connection)
        collar = pd.read_sql("SELECT * from collar", db_connection)
        desurveyed_assays = desurvey_assay(assay, survey, collar)
        print(desurveyed_assays.columns)
        desurveyed_assays.to_sql("desurveyed_assay", db_connection)
        return "Assay Desurvey Complete"
    else:
        raise PreventUpdate
