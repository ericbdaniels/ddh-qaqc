import dash
import sqlite3
import dash_bootstrap_components as dbc
from config.router import Router


app = dash.Dash(
    external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True
)
router = Router()
router.register_callbacks(app)
db_connection = sqlite3.connect(":memory:", check_same_thread=False)
