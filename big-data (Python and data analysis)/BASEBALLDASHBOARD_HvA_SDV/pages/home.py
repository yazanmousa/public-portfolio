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
from IPython.display import HTML, IFrame 

# df_career = pd.read_csv('datasets/db_batting_career.csv')
# df_yearly = pd.read_csv('datasets/db_batting_yearly.csv')

layout = html.Div([
    html.Header([
    html.Div([
    html.H1('Home', id='title'),
    ], className='header'),

        dbc.Container([
            dbc.Row([
                dbc.Col(html.H1("Welcome to the Sports Data Valley Baseball dashboard", className="home-titel"))
            ]),

            html.Div([
            html.Iframe(width="850" ,height="400" ,src="https://www.youtube.com/watch?v=NMFJopr3FoM"),
            ], className='youtube-video'),

            dbc.Row([
                dbc.Col(html.H5(children='')
                        , className="home-tekst")
            ]),

            dbc.Row([
                dbc.Col(dbc.Card(children=[html.H3(children='Learn More about Sports Data Valley (SDV)',
                                                className="text-center"),
                                        dbc.Button("SDV",
                                                    href="https://www.sportinnovator.nl/sport-data-valley/",
                                                    color="primary",
                                                    className="mt-3"),
                                        ],
                                body=True, color="dark", outline=True)
                        , className="home-blokken"),

                dbc.Col(dbc.Card(children=[html.H3(children='Access the code used to build this dashboard',
                                                className="text-center"),
                                        dbc.Button("GitHub",
                                                    href="#",
                                                    color="primary",
                                                    className="mt-3"),
                                        ],
                                body=True, color="dark", outline=True)
                        , className="home-blokken"),

                dbc.Col(dbc.Card(children=[html.H3(children='Read the documentation of this application',
                                                className="text-center"),
                                        dbc.Button("Documentation",
                                                    href="#",
                                                    color="primary",
                                                    className="mt-3"),

                                        ],
                                body=True, color="dark", outline=True)
                        , className="home-blokken")
            ], className="mb-5"),

            html.A("")

        ])

    ])

])

