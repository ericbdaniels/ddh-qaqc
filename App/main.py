from app import app, router, db_connection
from pages import template, upload, data_table, home, desurvey, composite, eda
from utils import misc


@router.route("/")
def index():
    return template.layout(home.readme_text)


@router.route("/upload")
def upload_page():
    return template.layout(upload.modal)


@router.route("/table/<table_name>")
def tables_page(table_name):
    return template.layout(data_table.table_view(table_name))


@router.route("/desurvey")
def desurvey_page():
    if misc.check_tables(db_connection):
        return template.layout(desurvey.content)
    else:
        return template.layout("DB ERROR")


@router.route("/composite")
def composite_page():
    return template.layout(composite.load_content(db_connection))


@router.route("/eda-univariate")
def univariate_eda_page():
    return template.layout(eda.load_page(db_connection))


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-d", "--desktop", help="Run as a desktop App", action="store_true"
    )
    args = parser.parse_args()
    if args.desktop:
        from pyfladesk import init_gui

        init_gui(
            app.server,
            port=5000,
            width=1200,
            height=800,
            window_title="DDH-QAQC",
            icon="App/assets/favicon.ico",
            argv=None,
        )
    else:
        app.run_server(debug=True)