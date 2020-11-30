from app import app, router
from pages import template, upload, data_table, home


@router.route("/")
def index():
    return template.layout(home.readme_text)


@router.route("/upload")
def upload_page():
    return template.layout(upload.modal)


@router.route("/table/<table_name>")
def tables_page(table_name):
    return template.layout(data_table.table_view(table_name))


if __name__ == "__main__":
    app.run_server(debug=True)
