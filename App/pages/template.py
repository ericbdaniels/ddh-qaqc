import dash_bootstrap_components as dbc

table_views = [
    dbc.DropdownMenuItem(f"View Table: {name}", href=f"/table/{name}")
    for name in ["assay", "collar", "survey", "desurvey"]
]

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Upload", href="/upload"),
                dbc.DropdownMenuItem("Desurvey", href="/desurvey"),
                dbc.DropdownMenuItem("Composite", href="/composite"),
            ]
            + table_views,
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="DDH-QAQC",
    brand_href="/",
    color="primary",
    dark=True,
)


def layout(content):
    return dbc.Container(children=[navbar, content], fluid=True)
