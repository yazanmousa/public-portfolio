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
pitchingDf = pd.read_sql_table('db_Pitching_Career', SQL_Engine)

# Round numeric values to 3 decimals
pitchingDf = pitchingDf.round(3)

# Rename column names
pitchingDf = pitchingDf.rename(columns={'era_label':'ERA', 'whip_label':'WHIP', 'so9_label':'SO9'})
pitchingDf = pitchingDf[{'PlayerName','ERA', 'WHIP', 'SO9'}]
pitchingDf.reset_index(drop = True)

# Fixed position of the columns
pitchingDf = pitchingDf[['PlayerName', 'ERA', 'WHIP', 'SO9']]
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
            dbc.Alert("Table is rendering, please wait a moment...", color="warning", id="feedbackPitching")
        ])
    ]),

    html.Div([
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
        # weight of ERA
        html.Div([
            html.Label('ERA weight: ', className='label-attribute'),
            dcc.Dropdown(
                id='mvp-input-era',
                options=options,
                placeholder='ERA',
                className= 'dropdown-attribute',
                value = 1
            )     
        ]),
        # weight of WHIP
        html.Div([
            html.Label('WHIP weight: ', className='label-attribute'),
            dcc.Dropdown(
                id='mvp-input-whip',
                options=options,
                placeholder='WHIP',
                className='dropdown-attribute',
                value = 1
            )
        ]),
        # weight of SO9
        html.Div([
            html.Label('SO9 weight: ', className='label-attribute'),
            dcc.Dropdown(
                id='mvp-input-so9',
                options= options,
                className='dropdown-attribute-year',
                placeholder='SO9',
                value = 1
            )
        ]),
    ]),

    # Table
    dbc.Row([
        dbc.Col([
            html.Div([
                dt.DataTable(
                    id='mvp-pitching-player-table',
                    style_cell={'textAlign': 'center'},
                    style_header={'fontWeight': 'bold'},
                    columns=[
                                    {"name": i, "id": i} for i in pitchingDf.columns
                    ],
                    data=pitchingDf.to_dict('records'),
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
        ], id='mvp-pitching-plot', width=  3)
    ])
])

# Callback to manage the player table and feedback
@app.callback(
    [Output('mvp-pitching-player-table', 'data'),
    Output('mvp-pitching-plot', 'style'),
    Output("feedbackPitching", "children"),
    Output("feedbackPitching", "color")],
    [Input('mvp-input-player-count', 'value'),
    Input('mvp-input-era', 'value'),
    Input('mvp-input-whip', 'value'),
    Input('mvp-input-so9', 'value')])
def update_output(rows, eraWeight, whipWeight, so9Weight):
    # Instantiate pitchingDf globally
    global pitchingDf

    # Converting type to float
    pitchingDf['ERA'] = pitchingDf['ERA'].astype(float)
    pitchingDf['WHIP'] = pitchingDf['WHIP'].astype(float)
    pitchingDf['SO9'] = pitchingDf['SO9'].astype(float)

    # Adding Average column to dataframe with the given weights
    pitchingDf["MVPAVG"] = ((pitchingDf.ERA * eraWeight)+ (pitchingDf.WHIP * whipWeight) + (pitchingDf.SO9 * so9Weight)) / 3
    
    # Sort the dataframe so the player with highest average comes first
    pitchingDf = pitchingDf.sort_values('MVPAVG', ascending = False)

    # Check if rows are empty or 0, if so don't show any players
    if (rows == None or rows <= 0):
        return (pitchingDf.head(0).to_dict('records'), {"display" : "None"}, "Table is rendered, please select number of players", "primary")
    table = pitchingDf.head((rows)).to_dict('records')
    return (table, {"display" : "block"}, "MVP is Calculated! Select player to view the stats in the bar chart", "success")

# Callback for plots
@app.callback(
    Output('mvp-pitching-plot', 'children'),
    [Input('mvp-pitching-player-table', 'selected_row_indices'),
    Input('mvp-pitching-player-table', 'selected_rows')])
def plotGraph(selected_row_indices, selected_rows):
    dataframe = pd.DataFrame(columns=('PlayerName','ERA', 'WHIP', 'SO9'))
    if len(selected_rows) > 0:
        for i in selected_rows:
            player = pitchingDf.iloc[i]
            dataframe.loc[i] = player
    return [
        dcc.Graph(
            figure={
                'data': [
                    {
                        'x': 'ERA',
                        'y': dataframe["ERA"],
                        'type': 'bar',
                        'marker': {'color': '#FF6961'},
                        'name': 'ERA'
                    }, {
                        'x': 'WHIP',
                        'y': dataframe["WHIP"],
                        'type' : 'bar',
                        'marker': {'color': '#89C689'},
                        'name': 'WHIP'

                    },
                    {
                        'x': 'SO9',
                        'y': dataframe["SO9"],
                        'type' : 'bar',
                        'marker': {'color': '#26ABFF'},
                        'name': 'SO9'
                    }
                ],
                'layout': {
                    'title': 'Player ' + dataframe["PlayerName"],
                    'margin': {'t': 10, 'l': 10, 'r': 10},

                }
            },
        )
    ]

