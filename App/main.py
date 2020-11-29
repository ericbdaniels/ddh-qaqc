from config.router import Router
import dash_core_components as dcc
import dash_html_components as html
from pages.template import template_layout
import dash_bootstrap_components as dbc
from app import app, router
from pages import upload
from dash.dependencies import Input, Output, State, ALL



@router.route("/")
def index():
    return template_layout(dbc.Container([html.Div(id="test-div"), upload.modal]))



if __name__ == "__main__":
    app.run_server(debug=True)    