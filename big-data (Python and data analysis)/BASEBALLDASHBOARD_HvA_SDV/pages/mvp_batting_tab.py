#pylint: disable = line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order

import dash
import dash_core_components as dcc
import dash_table as dt
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import pathlib
from server import app
from MySQL_data import SQL_Engine, execute_command, load_SQL_table
import json
import dash_bootstrap_components as dbc

import pandas as pd
from sqlalchemy import create_engine

###################################
host = "oege.ie.hva.nl"
username = "minderb002"
password = "+#/tRfRM5zwhnN"
database = "zminderb002"

config = "mysql+mysqlconnector://" + username + ":" + password + "@" + host + "/" + database

SQL_Engine = create_engine(config)
###################################

# Import datasets
battingDf = pd.read_sql_table('db_Batting_Career', SQL_Engine) 

# Round numeric values to 3 decimals
battingDf = battingDf.round(3)

# Rename column names
battingDf = battingDf.rename(columns={'avg_label':'BA', 'obp_label':'OBP', 'slg_label':'SLG'})
battingDf = battingDf[{'PlayerName','BA', 'OBP', 'SLG'}]
battingDf.reset_index(drop = True)

# Fixed position of the columns
battingDf = battingDf[['PlayerName', 'BA', 'OBP', 'SLG']]
options = [
    {'label': 1, 'value': 1},
    {'label': 2, 'value': 2},
    {'label': 3, 'value': 3},
    {'label': 4, 'value': 4},
    {'label': 5, 'value': 5},
]
# Layout dash page
layoutTab = html.Div([

    # Feedback row for alerts
    dbc.Row([
        dbc.Col([
            dbc.Alert("Table is rendering, please wait a moment...", color="warning", id="feedbackBatting")
        ])
    ]),

    # Input for selecting the number of players
    html.Div([
        html.Label('Select number of players: ', className='label-attribute'),
        dcc.Input(
            id='mvp-input-player-count',
            className= 'dropdown-attribute2',
            type='number',
            placeholder=''
        )
    ]),
    # weight of BA
    html.Div([
        html.Label('BA weight: ', className='label-attribute'),
        dcc.Dropdown(
            id='mvp-input-ba',
            options=options,
            placeholder='BA',
            className= 'dropdown-attribute',
            value = 1
        )     
    ]),

    # weight of OBP
    html.Div([
        html.Label('OBP weight: ', className='label-attribute'),
        dcc.Dropdown(
            id='mvp-input-obp',
            options=options,
            placeholder='OBP',
            className='dropdown-attribute',
            value = 1
        )
    ]),

    # weight of SLG
    html.Div([
        html.Label('SLG weight: ', className='label-attribute'),
        dcc.Dropdown(
            id='mvp-input-slg',
            options= options,
            className='dropdown-attribute-year',
            placeholder='SLG',
            value = 1
        )
    ]),

    # Table
    dbc.Row([
            dbc.Col([
                html.Div([
                    dt.DataTable(
                        id='mvp-batting-player-table',
                        style_cell={'textAlign': 'center'},
                        style_header={'fontWeight': 'bold'},
                        columns=[
                                        {"name": i, "id": i} for i in battingDf.columns
                        ],
                        data=battingDf.to_dict('records'),
                        virtualization=True,
                        editable=False,
                        sort_action="native",
                        sort_mode="multi",
                        column_selectable=False,
                        row_selectable='single',
                        row_deletable=False,
                        selected_columns=[],
                        selected_rows=[],
                        page_action="native",
                        page_current= 0,
                        fixed_rows={'headers': True},
                        page_size= 15,
                    )
                ], className='player-table-css'),
            ], width = 9),

            dbc.Col([
            ], id='mvp-batting-plot', width=  3)
        ])
    ])

# Callback to manage the player table and feedback
@app.callback(
    [Output('mvp-batting-player-table', 'data'),
    Output('mvp-batting-plot', 'style'),
    Output("feedbackBatting", "children"),
    Output("feedbackBatting", "color")],
    [Input('mvp-input-player-count', 'value'),
    Input('mvp-input-ba', 'value'),
    Input('mvp-input-obp', 'value'),
    Input('mvp-input-slg', 'value')])
def update_output(rows, baWeight, obpWeight, slgWeight):
    # Instantiate battingDf globally
    global battingDf

    # Converting type to float
    battingDf['BA'] = battingDf['BA'].astype(float)
    battingDf['OBP'] = battingDf['OBP'].astype(float)
    battingDf['SLG'] = battingDf['SLG'].astype(float)

    # Adding Average column to dataframe with the given weights
    battingDf["MVPAVG"] = ((battingDf.BA * baWeight)+ (battingDf.OBP * obpWeight) + (battingDf.SLG * slgWeight)) / 3

    # Sort the dataframe so the player with highest average comes first
    battingDf = battingDf.sort_values('MVPAVG', ascending = False)

    # Check if rows are empty or 0, if so don't show any players
    if (rows == None or rows <= 0):
        return (battingDf.head(0).to_dict("records"), {"display" : "None"}, "Table is rendered, please select number of players", "primary")
    table = battingDf.head((rows)).to_dict('records')
    return (table, {"display" : "block"}, "MVP is Calculated! Select player to view the stats in the bar chart", "success")

# Callback for plots
@app.callback(
    Output('mvp-batting-plot', 'children'),
    [Input('mvp-batting-player-table', 'selected_row_indices'),
    Input('mvp-batting-player-table', 'selected_rows')])
def plotGraph(selected_row_indices, selected_rows):
    dataframe = pd.DataFrame(columns=('PlayerName', 'BA', 'OBP', 'SLG'))
    if len(selected_rows) > 0:
        for i in selected_rows:
            player = battingDf.iloc[i]
            dataframe.loc[i] = player
    return [
            dcc.Graph(
                figure={
                    'data': [
                        {
                            'x': 'BA',
                            'y': dataframe["BA"],
                            'type': 'bar',
                            'marker': {'color': '#FF6961'},
                            'name': 'BA'
                        }, {
                            'x': 'OBP',
                            'y': dataframe["OBP"],
                            'type' : 'bar',
                            'marker': {'color': '#89C689'},
                            'name': 'OBP'

                        },
                        {
                            'x': 'SLG',
                            'y': dataframe["SLG"],
                            'type' : 'bar',
                            'marker': {'color': '#26ABFF'},
                            'name': 'SLG'
                        }
                    ],
                    'layout': {
                        'title': 'Player ' + dataframe["PlayerName"],
                        'margin': {'t': 10, 'l': 10, 'r': 10},

                    }
                },
            )]
