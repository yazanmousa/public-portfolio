#pylint: disable = line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table as dt
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import pathlib
from server import app
from pages import attribute_batting_tab, attribute_pitching_tab

# Layout dash page
layout = html.Div([
    # Nav bar
    html.Header([
        html.H1('Top statistics', id='title')
    ], className='header'),

    # Tab menu
    html.Div([
        dcc.Tabs(id='attribute-tab', value='batting_tab', children=[
            dcc.Tab(label='Batting data', value='batting_tab'),
            dcc.Tab(label='Pitching data', value='pitching_tab')
        ], className='attribute-tab-css'),

        # More information
        html.Div([
            dbc.Button(
                'Click here to learn more about filtering',
                id='more-info-button', className='attribute-info-button'
            ),

            dbc.Collapse([
                dbc.Card(
                    dbc.CardBody('''Use basic operators to filter the table, like:
                                '=2020' in the year column to only see data from season 2020 or
                                '>50' in the Innings Pitched (IP) column to only show player who have pitched more than 50 innings.
                                Usable operators are Equal: =, Bigger than: >, Smaller than: <.
                                It's also possible to filter ons strings for the columns: 'Name', 'League'.''')
                )], id='filter-collapse', className='attribute-info-text'),
        ], className='attribute-info'),

        # Tab content
        html.Div(id='attribute-tab-content')
    ]),


])

# Collapse
@app.callback(
    Output('filter-collapse', 'is_open'),
    [Input('more-info-button', 'n_clicks')],
    [State('filter-collapse', 'is_open')]
)
def toggle_popover_filter(n, is_open):
    if n:
        return not is_open
    return is_open

# Load tab content
@app.callback(
    Output('attribute-tab-content', 'children'),
    Input('attribute-tab', 'value')
)
def render_content(tab):
    if tab == 'batting_tab':
        return attribute_batting_tab.layout
    elif tab == 'pitching_tab':
        return attribute_pitching_tab.layout


