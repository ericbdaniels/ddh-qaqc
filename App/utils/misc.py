from app import db_connection
import dash_table


def check_tables(conn):
    cursor = conn.cursor()
    for table_name in ["assay", "collar", "survey"]:
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
        except:
            return False
    return True


def load_table(df):
    return dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=100,
        export_format="csv",
    )