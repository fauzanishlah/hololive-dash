import dash_bootstrap_components as dbc

Navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Branch", href="/branch", active="exact")),
        # dbc.NavItem(dbc.NavLink("Gen", href="/gen", active="exact")),
        dbc.NavItem(dbc.NavLink("Talent", href="/talent", active="exact")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Source", header=True),
                dbc.DropdownMenuItem("github", target="_blank", href="https://github.com/fauzanishlah/hololive-dash"),
                dbc.DropdownMenuItem("notebook", target="_blank", href="https://github.com/fauzanishlah/hololive-dash/tree/main/notebook"),
            ],
            nav=True,
            in_navbar=True,
            label="Source Code",
        ),
    ],
    brand="Hololive Youtube Analysis",
    brand_href="/",
    color="secondary",
    # dark=True,
)