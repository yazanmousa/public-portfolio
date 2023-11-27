#pylint: disable = line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order

from dash import dependencies
import plotly.graph_objects as go
import pandas as pd
import dash_table
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from MySQL_data import SQL_Engine, execute_command, load_SQL_table
from dash.exceptions import PreventUpdate
from sqlalchemy import select
from server import app
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import urllib
# from playerscraper.playerScraper import getData
from .playerscraper import playerScraper


import mysql.connector
mydb = mysql.connector.connect(
  host="oege.ie.hva.nl",
  user="minderb002",
  password="+#/tRfRM5zwhnN",
  database="zminderb002"
)

################################### 
import pandas as pd
from sqlalchemy import create_engine
# from MySQL_data import SQL_Engine

host = "oege.ie.hva.nl"
username = "minderb002"
password = "+#/tRfRM5zwhnN"
database = "zminderb002"

config = "mysql+mysqlconnector://" + username + ":" + password + "@" + host + "/" + database

SQL_Engine = create_engine(config)
###################################

# Retrieve data from Player table in db
# Clean it up, and set header to uppercase
players = pd.read_sql_table('Player', SQL_Engine)
players.rename(columns={'fullName': 'playername', 'id' : 'ID'}, inplace=True)
players=players[{'playername', 'ID'}]
players["league"] = "NaN"
players.columns = map(lambda x: str(x).upper(), players.columns)
players['PLAYERNAME'] = players['PLAYERNAME'].astype('category')

# Retrieve data from allplayers table in db
# Clean it up and set header to uppercase
milb_mlb_players = pd.read_sql_table('allplayers', SQL_Engine)
milb_mlb_players.rename(columns={'Name': 'playername', 'Id' : 'ID', 'league':'League'}, inplace=True)
milb_mlb_players=milb_mlb_players[{'playername', 'ID', 'League'}]
milb_mlb_players.columns = map(lambda x: str(x).upper(), milb_mlb_players.columns)
milb_mlb_players['PLAYERNAME'] = milb_mlb_players['PLAYERNAME'].astype('category')

# Combine both dataframes
# Sort items on league, so NAN comes last
# Delete duplicate entries based on Name 
allPlayersCombined = pd.concat([players,milb_mlb_players], ignore_index=True).sort_values("LEAGUE").drop_duplicates(subset="PLAYERNAME", keep=False)
# Delete all players with league = NaN, because these players already exists in the list
allPlayersCombined = allPlayersCombined[allPlayersCombined.LEAGUE != 'NaN']
allPlayersCombined = allPlayersCombined[['PLAYERNAME', 'ID', 'LEAGUE']]

layout = html.Div([
        html.Header([
        html.H1('Add Players', id='title')
    ], className='header'),

    dbc.Row(dbc.Col(
            dcc.Tabs(id='attribute-tab', value='batting_tab', children=[
            dcc.Tab(label='Batting & Pitching playerlist', value='batting_tab'),
        ], className='attribute-tab-css'),
    )),
    html.Br(),
    # Feedback row for alerts
    dbc.Row([
        dbc.Col([
            dbc.Alert("No players selected or button is not clicked!", color="warning", id="feedback", style={"display": "block"})
        ])
    ]),
    

    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H3('Add Player'),
            html.Br()],
            width = 9),
        dbc.Col([
            html.Br(),
            html.H3('Selected Players', id="SelectedPlayersText"),
            html.Br()]
            )
        ]),

    dbc.Row(children=[dbc.Col(
        dash_table.DataTable(
            id='table_batting',
            columns=[
                {"name": i, "id": i} for i in allPlayersCombined.columns
            ],
            style_table={'overflowy': 'scroll', 'height': 'auto', 'width' : 'auto'},
            style_cell={'whiteSpace': 'normal', 'textAlign': 'left', 'padding': '10px'},
            data=allPlayersCombined.to_dict('records'),
            virtualization=True,
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            # column_selectable=False,
            row_selectable="multi",
            row_deletable=False,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 200,
            # fill_width=False,
            # Makes the header of the table bold
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            fixed_rows={'headers': True},
            # align text columns to left. By default they are aligned to right, the cells with numbers will be allighed to the left
            style_cell_conditional=[{
                'if': {'column_id': c},
                'textAlign': 'left',
            } for c in ['PLAYERNAME']],
            # style odd rows to have a grey-ish background color
            style_data_conditional=[{
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)',
            }],
        ), width= 9),

        html.Div([], id="selected-players")

    ]),

    dbc.Row(
        dbc.Col(
            dbc.Button("Save changes", color="primary", id="savePlayersButton", className="mr-1", block=True), width = 9)
            ),
])

# Check for selected rows 
@app.callback(
    [Output('selected-players','children'),
    Output('selected-players', 'style'),
    Output('SelectedPlayersText', 'style'),
    Output('savePlayersButton', 'style')],
    [Input('table_batting', 'selected_row_indices'),
    Input('table_batting', 'selected_rows'),
    Input('savePlayersButton', 'n_clicks')])
def f(selected_row_indices, selected_rows, n_clicks):
    # selected_rows = [1, 3]
    # Set headers for dataframe
    selectedPlayersData = pd.DataFrame(columns=('Name', 'Id', 'League'))
    # Getting player data using the index of the dataframe and selected row
    for i in selected_rows:
        player = allPlayersCombined.iloc[i].to_list()

        # Add selected player to dataframe
        selectedPlayersData.loc[i] = player
    # Convert dataframe to CSV
    selectedPlayersData.to_csv("BASEBALLDASHBOARD_HvA_SDV/pages/playersToDatabase.csv", index=False)
    list = selectedPlayersData.values.tolist()
    selectedPlayer = [dbc.ListGroupItem(x) for x in list]
    selectedList = dbc.ListGroup([dbc.ListGroupItem(selectedPlayer)])
    # print(list)

    # Check whether there are selected players if not, hide elements
    if len(selected_rows) != 0:
        elementsStyle = {"display" : "block"}
    else:
        elementsStyle = {"display" : "none"}

    return [selectedList, elementsStyle, elementsStyle, elementsStyle]

# Check if the button is clicked, and read csv
@app.callback(
    [dash.dependencies.Output('selected-players', 'column')],
    # dash.dependencies.Output('feedback', 'children'),
    # dash.dependencies.Output('feedback', 'color')],
    dash.dependencies.Input('savePlayersButton', 'n_clicks'))
def update_output(n_clicks):
    csv = pd.read_csv('BASEBALLDASHBOARD_HvA_SDV/pages/playersToDatabase.csv', sep=',')
    if (n_clicks is None):
        n_clicks = 0
        # return [str(csv), "No players selected or button is not clicked!", "warning"]
        return [str(csv)]
    else:
        print("n_clicks: " + str(n_clicks))
        csvList = csv.values.tolist()
        for i in range(len(csvList)):
            playerScraper.getData(csvList[i][0], csvList[i][1], csvList[i][2])
        # return [str(csv), "Players are being inserted, please don't refresh the page! Page will refresh automatically the action is performed", "primary"]
        return [str(csv)]

@app.callback(
    [dash.dependencies.Output('feedback', 'children'),
    dash.dependencies.Output('feedback', 'color')],
    dash.dependencies.Input('savePlayersButton', 'n_clicks'))
def update_output(n_clicks):
    if not(n_clicks is None):
        # return["Players are being inserted in the database, please do not refresh page! Page will refresh automatically once the action is perfromed!", "primary"]
        return["Players are being inserted into the database. It will take approximately 30 seconds per player. You can keep navigating the application in the meantime", "primary"]
    else:
        return["No players selected or button is not clicked!", "warning"]


@app.callback(
    dash.dependencies.Output('savePlayersButton', 'disabled'),
    dash.dependencies.Input('savePlayersButton', 'n_clicks'))
def disableButton(n_clicks):
    if not(n_clicks is None):
        return True
    else:
        return False
