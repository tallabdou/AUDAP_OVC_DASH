import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
import dash
import dash_core_components as dcc
from colleges import college_layout
from ut import ut_layout
from simulation import simulations_layout
from colleges_palois import colleges_palois_layout
from ut_des_colleges_palois import ut_des_colleges_palois_layout

def app_dash_file(app): 
    navbar = dbc.Navbar(
                dbc.Container([
                    dbc.Row([
                        dbc.Col([
                            # html.Img(src=dash.get_asset_url('logo2.png'), height="40px"),
                            dbc.NavbarBrand("Simulation OVC 64", className="ms-2")
                        ],
                        width={"size":"auto"})
                    ],
                    align="center",
                    className="g-0"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Nav([
                                dbc.NavItem(dbc.DropdownMenu(
                                children=[
                                    dbc.DropdownMenuItem("Collège", href="/ovc64/college"),
                                    dbc.DropdownMenuItem("Unité territoriale", href="/ovc64/ut")
                                ],
                                nav=True,
                                in_navbar=True,
                                label="Collège/UT",
                            )),
                        dbc.NavItem(dbc.NavLink("Simulation IPS ", href="/ovc64/simulationsips")),
                                ############################################################################
                                dbc.NavItem(dbc.DropdownMenu(
                                children=[
                                    dbc.DropdownMenuItem("Collèges palois", href="/ovc64/colleges_palois"),
                                    dbc.DropdownMenuItem("UT des collèges palois", href="/ovc64/ut_colleges_palois")
                                ],
                                nav=True,
                                in_navbar=True,
                                label="Analyse collèges palois",
                                )),
                                ######################################################
                                ],
                                navbar=True
                                ),
                                dbc.Collapse(id="navbar-collapse", navbar=True),
                            ],
                    width={"size":"auto"})
                ],
                align="center"),
                dbc.Col(dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)),
                    ],
                fluid=True
                ),
        color="primary",
        dark=True
    )

    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        navbar,
        html.Div(id='page-content')
    ])

    @app.callback(Output('page-content', 'children'),
                [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/ovc64/college':
            return college_layout
        elif pathname == '/ovc64/ut':
            return ut_layout
        elif pathname == '/ovc64/simulationsips':
            return simulations_layout
        elif pathname == '/ovc64/colleges_palois':
            return colleges_palois_layout
        elif pathname == '/ovc64/ut_colleges_palois':
            return ut_des_colleges_palois_layout
        # else:
        #     # Si l'URL n'est pas valide, redirigez l'utilisateur vers une page spécifique ou renvoyez un message d'erreur
        #     return html.Div(["La page demandée n'existe pas"])
