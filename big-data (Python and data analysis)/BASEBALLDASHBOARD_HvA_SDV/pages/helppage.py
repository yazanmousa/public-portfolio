#pylint: disable = line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pathlib
import dash_bootstrap_components as dbc
from server import app


layout = html.Div([
    html.Header([
    html.Div([
    html.H1('Help', id='title'),
    ], className='header'),

        # html.Div([
        # html.Img(src=app.get_asset_url('knbsb-logo.png')),
        # ], className='foto-ding'),

        ]),

    dbc.Container([
            
            dbc.Row([
                dbc.Col(html.H2(children='Techdnical and User manual'
                                        )
                        , className="helptitle")
                ]),                

            dbc.Row([
                dbc.Col(html.H5(children='On this page you can find different links to the manual which explains you how to use the dashboard and the code behind the dashboard itself. You can also contact the developers if you have any more questions.'
                                        )
                        , className="helpdesc")
                ]),                

            dbc.Row([
                dbc.Col(dbc.Card(children=[html.H3(children='Access the code used to build this dashboard',
                                                className="text-center"),
                                        dbc.Button("GitHub",
                                                    href="",
                                                    color="primary",
                                                    className="bloktekst"),
                                        ],
                                body=True, color="dark", outline=True)
                        , className="help-blokken"),

                dbc.Col(dbc.Card(children=[html.H3(children='Read the documentation of this application',
                                                className="text-center"),
                                        dbc.Button("Documentation",
                                                    href="https://docs.google.com/document/d/1utMlWJteSezia9NM1zStPpWaDFNo1s1sj6WWjmr03Ws/edit",
                                                    target="_blank",
                                                    color="primary",
                                                    className="bloktekst"),

                                        ],
                                body=True, color="dark", outline=True)
                        , className="help-blokken")
            ], className="mb-5"),

            dbc.Row([
                dbc.Col(html.H5(children='Contact information: '
                                        )
                        , className="contactdesc")
                ]),

    ])

])