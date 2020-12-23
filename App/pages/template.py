import dash_bootstrap_components as dbc

table_views = [
    dbc.DropdownMenuItem(f"{name}", href=f"/table/{name.lower()}")
    for name in ["Assay", "Collar", "Survey", "Desurvey", "Composites"]
]

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Operations", header=True),
                dbc.DropdownMenuItem("Upload", href="/upload"),
                dbc.DropdownMenuItem("Desurvey", href="/desurvey"),
                dbc.DropdownMenuItem("Composite", href="/composite"),
            ]
            + [
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Tables", header=True),
            ]
            + table_views
            + [
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Data Analysis", header=True),
                dbc.DropdownMenuItem("Composite Length", href="/eda-univariate"),
            ],
            nav=True,
            in_navbar=True,
            label="Navigation",
        ),
    ],
    brand="DDH-QAQC",
    brand_href="/",
    color="primary",
    dark=True,
)


def layout(content):
    return dbc.Container(children=[navbar, content], fluid=True)
