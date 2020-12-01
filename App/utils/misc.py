from app import db_connection


def check_tables(conn):
    cursor = conn.cursor()
    for table_name in ["assay", "collar", "survey"]:
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
        except:
            return False
    return True