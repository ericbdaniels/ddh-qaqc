import dash_bootstrap_components as dbc
import dash_core_components as dcc


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("QA/QC", href=""),
                dbc.DropdownMenuItem("Compositing", href=""),
                dbc.DropdownMenuItem("Data Exploration", href="")
            ],
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


def template_layout(content):
    return dbc.Container(children=[navbar, content], fluid=True)
