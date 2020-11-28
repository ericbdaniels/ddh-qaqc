import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def create_uploader(id_name):
    uploader = dcc.Upload(
        id={"type":"upload","name":id_name},
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
            dbc.Tab(tab_survey_content, label="Sruvey")
        ])
    ])
], size="lg", is_open=True, centered=True, autoFocus=True)