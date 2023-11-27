#pylint: disable = line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import pathlib
from server import app
from pages import mvp_batting_tab, mvp_pitching_tab

# Layout dash page
layout = html.Div([

    # Nav bar
    html.Header([
        html.H1('Most Valuable Player', id='title')
    ], className='header'),

   
    dbc.Row(dbc.Col(
            dcc.Tabs(id='attribute-tab', value='batting_tab', children=[
            dcc.Tab(label='Batting data', value='batting_tab'),
            dcc.Tab(label='Pitching data', value='pitching_tab')
        ], className='attribute-tab-css'),
    )),
   
    
    html.Br(),

    html.Div(id='tab')
])

@app.callback(
    Output('tab', 'children'),
    Input('attribute-tab', 'value')
)
def render_content(tab):
    if tab == 'batting_tab':
        return mvp_batting_tab.layoutTab
    elif tab == 'pitching_tab':
        return mvp_pitching_tab.layoutTab
      
# @app.callback(
#     Output('plot', 'children'),
#     Input('attribute-tab', 'value')
# )
# def render_content_plot(plot):
#     if plot == 'batting_tab':
#         return mvp_batting_tab.layoutPlot
#     elif plot == 'pitching_tab':
#         return mvp_pitching_tab.layoutPlot


