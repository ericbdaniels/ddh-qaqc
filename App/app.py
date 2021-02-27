import sys
from collections import namedtuple

import pkg_resources

IS_FROZEN = hasattr(sys, "_MEIPASS")

# backup true function
_true_get_distribution = pkg_resources.get_distribution
# create small placeholder for the dash call
# _flask_compress_version = parse_version(get_distribution("flask-compress").version)
_Dist = namedtuple("_Dist", ["version"])


def _get_distribution(dist):
    if IS_FROZEN and dist == "flask-compress":
        return _Dist("1.5.0")
    else:
        return _true_get_distribution(dist)


# monkey patch the function so it can work once frozen and pkg_resources is of
# no help
pkg_resources.get_distribution = _get_distribution


import dash
import sqlite3
import dash_bootstrap_components as dbc
from config.router import Router


app = dash.Dash(
    external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True
)
app.title = "DDH-QAQC"
router = Router()
router.register_callbacks(app)
# db_connection = sqlite3.connect(":memory:", check_same_thread=False)
db_connection = sqlite3.connect("composites.db", check_same_thread=False)
