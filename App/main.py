from app import app, router
from pages import template_layout, upload, data_table


@router.route("/")
def index():
    return template_layout("WHOOP WHOOP")


@router.route("/upload")
def upload_page():
    return template_layout(upload.modal)


@router.route("/table/<table_name>")
def tables_page(table_name):
    return template_layout(data_table.table_view(table_name))


if __name__ == "__main__":
    app.run_server(debug=True)
