import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from router import Router
from template import template_layout
import plots
import random

from urllib.parse import urlencode

app = dash.Dash(
    external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True
)

router = Router()
router.register_callbacks(app)


@router.route("/")
def index():
    return template_layout(html.Div("Home"))

@router.route("/upload")
def data_upload_page():
    from pages.upload import modal
    return template_layout(modal)


if __name__ == "__main__":
    app.run_server(debug=True)
