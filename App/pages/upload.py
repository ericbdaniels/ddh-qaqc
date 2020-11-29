import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import pandas as pd
import base64
import io
from app import app, db_connection

def parse_data(content, filename):
    content_string = content[0].split(".")[1].split(",")[-1]
    print("CONTENT STRING", content_string[:50])
    decoded = base64.b64decode(content_string)
    print(decoded[:50])
    if "csv" in filename:
        return  pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    elif "xls" in filename:
        return pd.read_excel(io.BytesIO(decoded))
    else:
        return None
    
@app.callback(
    Output("test-div","children"),
    [Input({'type':'upload','name':ALL},"contents"),
    Input({'type':'upload','name':ALL},"filename")]
)
def load_data_from_csv(content, filename):
    if filename[0] is None:
        raise PreventUpdate
    else:
        table_name = dash.callback_context.triggered[0]["prop_id"]
        print(table_name)
        df = parse_data(content, filename[0])
        df.to_sql(table_name, db_connection)
        return f"{filename} loaded to db ?"

def create_uploader(id_name):
    uploader = dcc.Upload(
        id={'type':'upload','name':id_name},
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        className="mx-auto",
        style={
            'width': '90%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
    )
    return uploader

tab_assay_content = dbc.Card([
    html.P("Select assay data for Upload (commonly assay.csv)"),
    create_uploader("assay")])

tab_collar_content = dbc.Card([
    html.P("Select collar data for Upload (commonly collar.csv)"),
    create_uploader("collar")])

tab_survey_content = dbc.Card([
    html.P("Select survey data for Upload (commonly survey.csv)"),
    create_uploader("survey")])

modal = dbc.Modal([
    dbc.ModalHeader("Select Files For Upload", className="p-2"),
    dbc.ModalBody(children=[
        dbc.Tabs([
            dbc.Tab(tab_assay_content, label="Assay"),
            dbc.Tab(tab_collar_content, label="Collar"),
            dbc.Tab(tab_survey_content, label="Survey")
        ])
    ])
], size="lg", is_open=True, centered=True, autoFocus=True)

