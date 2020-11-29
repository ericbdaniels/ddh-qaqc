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
    return template_layout("WHOOP WHOOP")

@router.route("/upload")
def upload_page():
    return template_layout(upload.modal)

@router.route("/table/<table_name>")
def tables_page(table_name):
    return template_layout(table_view(table_name))


if __name__ == "__main__":
    app.run_server(debug=True)    