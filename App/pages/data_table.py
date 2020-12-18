import dash_bootstrap_components as dbc
import pandas as pd
from app import db_connection
from utils.misc import load_table


def table_view(table_name):
    df = pd.read_sql(f"SELECT * from  {table_name}", db_connection)
    table = load_table(df)
    return dbc.Container([table], fluid=True)