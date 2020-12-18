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
        columns=[{"name": i, "id": i} for i in df.columns[1:]],
        data=df.to_dict("records"),
        editable=True,
        sort_action="native",
        filter_action="native",
        sort_mode="multi",
        column_selectable="single",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=25,
        export_format="csv",
        style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
        style_as_list_view=True,
        style_cell={"padding": "5px"},
        style_table={"overflowX": "auto"},
    )