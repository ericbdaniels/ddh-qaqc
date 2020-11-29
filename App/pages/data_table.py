import dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from app import db_connection


def load_table(df, name):
    return dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    )


def table_view(table_name):
    df = pd.read_sql(f"SELECT * from  {table_name}", db_connection)
    table = load_table(df, table_name)
    return dbc.Container([table])