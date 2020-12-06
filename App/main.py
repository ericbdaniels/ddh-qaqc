from app import app, router, db_connection
from pages import (
    template,
    upload,
    data_table,
    home,
    desurvey,
    composite,
    univariate_eda,
)
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
    return template.layout(univariate_eda.load_content(db_connection))


if __name__ == "__main__":
    app.run_server(debug=True)
