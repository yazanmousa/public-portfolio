#pylint: disable = line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order
from dash_html_components.Center import Center
from dash_html_components.H1 import H1
from dash_html_components.Hr import Hr
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import create_engine
from pandas import DataFrame, read_sql, read_csv, concat
from MySQL_data import SQL_Engine, execute_command, load_SQL_table
from MySQL_data import load_SQL_table
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table as dt
from dash.exceptions import PreventUpdate
from pandas import DataFrame, read_sql, read_csv, concat

from server import app

app.css.config.serve_locally = True

host = "oege.ie.hva.nl"
username = "minderb002"
password = "+#/tRfRM5zwhnN"
database = "zminderb002"

config = "mysql+mysqlconnector://" + username + ":" + password + "@" + host + "/" + database
SQL_Engine = create_engine(config)

# Format tournaments info
tournaments = pd.read_sql_table('tournaments', SQL_Engine)
allStatsTournaments = ['ab','r','h','2B','3B','hr','rbi','tb','avg','slg','obp','ops','bb','hbp','so','gdp','sf','sh','sb','cs']
tournamentsStatistics = pd.DataFrame(allStatsTournaments, columns = ['Statistics'])
tournamentsStatistics = tournamentsStatistics.squeeze()
tournamentsPlayerName = tournaments['Name']
tournamentsPlayerNameLowerCase = []

# Loop through playername of tournaments and format them (All lower case and firstname then lastname)
for i in range(len(tournamentsPlayerName)):
    name = tournamentsPlayerName.loc[i]
    nameElements = name.split(" ")
    correctName = []
    lowerCaseName = ""
    for j in range(len(nameElements)):
        capital = nameElements[j].isupper()
        if not(capital):
            correctName.append(nameElements[j])
    for k in range(len(nameElements)):
        capital = nameElements[k].isupper()
        if (capital):
            correctName.append(nameElements[k])
            
    for l in range(len(correctName)):
        lowerCaseName += correctName[l].lower().capitalize() + " "
      
    tournamentsPlayerNameLowerCase.append(lowerCaseName.strip())
    tournaments.at[i, "Name"] = tournamentsPlayerNameLowerCase[i]


tournamentsNames = pd.DataFrame(tournamentsPlayerNameLowerCase, columns = ['Name'])
tournamentsNames = tournamentsNames.squeeze()

    
# Format batting gamelogs 
gamelogBatting = pd.read_sql_table('db_Batting_Gamelogs', SQL_Engine)
gamelogBatting['PlayerName'] = gamelogBatting["PlayerName"].str.lower()
gamelogBatting["PlayerName"] = gamelogBatting["PlayerName"].str.title()
allStatsBatting = ['pa', 'ab', 'r', 'h', 'rbi', '2b', '3b', 'hr', 'bb', 'sb', 'cs', 'hbp', 'sh', 'sf', 'so', 'ibb', 'gdp', 'po', 'a', 'e', 'PosString', 'Pos_1b', 'Pos_2b', 'Pos_3b', 'Pos_c', 'Pos_cf', 'Pos_dh', 'Pos_lf', 'Pos_p', 'Pos_ph', 'Pos_pr', 'Pos_rf', 'Pos_ss', 'avg_value', 'avg_label', 'obp_value', 'obp_label', 'slg_value', 'slg_label', 'ops_value', 'ops_label', 'iso_value', 'iso_label']
battingStatistics = pd.DataFrame(allStatsBatting, columns = ['Statistics'])
battingStatistics = battingStatistics.squeeze()
gamelogBattingNames = gamelogBatting['PlayerName'].str.title()
gamelogBattingNames = gamelogBattingNames.drop_duplicates()

# Format pitching gamelogs
gamelogPitching = pd.read_sql_table('db_Pitching_Gamelogs', SQL_Engine)
gamelogPitching['PlayerName'] = gamelogPitching["PlayerName"].str.lower()
gamelogPitching['PlayerName'] = gamelogPitching["PlayerName"].str.title()
allStatsPitching = ["gs", "ip_value", "ip_label", "h", "r", "er", "bb", "so", "hbp", "ibb", "ab", "bf", "fo", "go", "np", "Win", "Loss", "Save", "era_value", "era_label", "wlp_value", "wlp_label", "whip_value", "whip_label", "h9_value", "h9_label", "bb9_value", "bb9_label", "so9_value", "so9_label", "sobb_value", "sobb_label"]
pitchingStatistics = pd.DataFrame(allStatsPitching, columns = ['Statistics'])
pitchingStatistics = pitchingStatistics.squeeze()
gamelogPitchingNames = gamelogPitching['PlayerName'].str.title()
gamelogPitchingNames = gamelogPitchingNames.drop_duplicates()

# Combine all dataframe to get 1 dataframe with all the playernames
allNames = pd.DataFrame
allNames = pd.concat([tournamentsNames, gamelogBattingNames, gamelogPitchingNames], ignore_index=True)
allNames = allNames.drop_duplicates()
allNames = allNames.str.title()

layout = html.Div([
    # Nav bar
    html.Header([
        html.H1('Tournaments', id='title')
    ], className='header'),
    
    html.Div([
        html.Br(),
        html.H2('Select player to retrieve data'),
            html.Div([
                dbc.Button(
                    'Click here to learn more about filtering',
                    id='more-info-button', className='attribute-info-button'
                ), 
                dbc.Collapse([
                    dbc.Card(
                        dbc.CardBody('''The selected player will be the selected player for all the datatables. All statistics are selected by default. If you would like to select specific statistics, you can do so through the dropdown. If the datatable does not show any data, the player does not have stats for the specific position.''')
                )], id='filter-collapse', className='attribute-info-text'),
            ], style={"float": "right"}),
        html.Br(),
    ]),

    html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Dropdown(
                            id='playerName', className='player-selection-league-dropdown', optionHeight=50,
                            options=[{'label': i, 'value': i} for i in allNames],
                            placeholder='Select a player', 
                        ),
                ], id='group-interval', className='data-table-knoppen'),
            ], style={"padding-left": "0px"}),
        ]),
    ], id='dropdown-content', style={"line-height" : "0px"}),

    html.Div([
        html.Div([
            html.H3('Tournaments'),
                    # html.Div([
                        html.P(['Select specific statistics']),
                        dcc.Dropdown(
                                id='statistics',className='player-selection-league-dropdown',
                                options=[{'label': i, 'value': i} for i in tournamentsStatistics], 
                                placeholder='--All--', multi=True),
                        # ], id='group-type', className='data-table-knoppen'),
                html.Div(id='tournamentsTable')
            ], className='data-table'),

        html.Div([
            html.Hr(),
            html.H3('Matches'),
            html.H5('Batting'),
            html.Div([
                html.P(['Select specific statistics']),
                dcc.Dropdown(
                        id='statsBatting', className='player-selection-league-dropdown',
                        options=[{'label': i, 'value': i} for i in battingStatistics],
                        placeholder='--All--', multi=True, 
                        ),
                ], id='group-interval', className='data-table-knoppen'),
            html.Div(id='matchesBattingTable'),
            html.Hr(),
            html.H5('Pitching'),
            html.Div([
                html.P(['Select specific statistics']),
                dcc.Dropdown(
                        id='statsPitching', className='player-selection-league-dropdown',
                        options=[{'label': i, 'value': i} for i in pitchingStatistics],
                        placeholder='--All--', multi=True, 
                        ),
                ], id='group-interval', className='data-table-knoppen'),
            html.Div(id='matchesPitchingTable')
        ], className='data-table'),
    ]),
])


@app.callback(
    dash.dependencies.Output('matchesBattingTable', 'children'),
    [dash.dependencies.Input('playerName', 'value'),
    dash.dependencies.Input('statsBatting', 'value')])
def loadMatchesBatting(playername, battingStat):
    if not(battingStat):
        battingStat = allStatsBatting

    prefix = ['PlayerName','Team','Opponent', 'League', 'SeasonType', "DateString"]
    
    columnsBatting = prefix + battingStat
    dfBatting = gamelogBatting.loc[gamelogBatting['PlayerName']==playername]
    dfBatting= dfBatting[columnsBatting]
    battingTable = [ # Table
    dbc.Row([
            dbc.Col([
                html.Div([
                    dt.DataTable(
                        id='batting-table',
                        style_cell={'textAlign': 'center'},
                        style_header={'fontWeight': 'bold'},
                        style_table={'overflowX': 'auto'},
                        columns=[
                                        {"name": i, "id": i} for i in dfBatting.columns
                        ],
                        data=dfBatting.to_dict('records'),
                        virtualization=True,
                        editable=False,
                        sort_action="native",
                        sort_mode="multi",
                        column_selectable=False,
                        row_deletable=False,
                        selected_columns=[],
                        selected_rows=[],
                        page_action="native",
                        page_current= 0,
                        fixed_rows={'headers': True},
                        page_size= 15,
                    )
                ], className='player-table-css'),
            ]),
        ])]
    return battingTable

@app.callback(
    dash.dependencies.Output('matchesPitchingTable', 'children'),
    [dash.dependencies.Input('playerName', 'value'),
    dash.dependencies.Input('statsPitching', 'value')])
def loadMatchesPitching(playername, pitchingStat):
    if not(pitchingStat):
        pitchingStat = allStatsPitching
    list = ['PlayerName','Team','Opponent', 'League', 'SeasonType', "DateString"]
    columnsPitching = list + pitchingStat
    dfPitching = gamelogPitching.loc[gamelogPitching['PlayerName']==playername]
    dfPitching= dfPitching[columnsPitching]     

    pitchingTable = [ # Table
    dbc.Row([
            dbc.Col([
                html.Div([
                    dt.DataTable(
                        id='pitching-table',
                        style_cell={'textAlign': 'center'},
                        style_header={'fontWeight': 'bold'},
                        style_table={'overflowX': 'auto'},
                        columns=[
                                        {"name": i, "id": i} for i in dfPitching.columns
                        ],
                        data=dfPitching.to_dict('records'),
                        virtualization=True,
                        editable=False,
                        sort_action="native",
                        sort_mode="multi",
                        column_selectable=False,
                        row_deletable=False,
                        selected_columns=[],
                        selected_rows=[],
                        page_action="native",
                        page_current= 0,
                        fixed_rows={'headers': True},
                        page_size= 15,
                    )
                ], className='player-table-css'),
            ]),
        ])]
    return pitchingTable


@app.callback(
    dash.dependencies.Output('tournamentsTable', 'children'),
    [dash.dependencies.Input('playerName', 'value'),
    dash.dependencies.Input('statistics', 'value')])
def loadTournament(playername, statistics): 
    if not(statistics) :
        statistics = allStatsTournaments
    list = ['Name','Year','Tournament']
    columns = list + statistics
    df2 = tournaments.loc[tournaments['Name']==playername]
    df2= df2[columns]
   
    return[ # Table
    dbc.Row([
            dbc.Col([
                html.Div([
                    dt.DataTable(
                        id='tournaments-table',
                        style_cell={'textAlign': 'center'},
                        style_header={'fontWeight': 'bold'},
                        style_table={'overflowX': 'auto'},
                        columns=[
                                        {"name": i, "id": i} for i in df2.columns
                        ],
                        data=df2.to_dict('records'),
                        virtualization=True,
                        editable=False,
                        sort_action="native",
                        sort_mode="multi",
                        column_selectable=False,
                        row_deletable=False,
                        selected_columns=[],
                        selected_rows=[],
                        page_action="native",
                        page_current= 0,
                        fixed_rows={'headers': True},
                        page_size= 15,
                    )
                ], className='player-table-css'),
            ]),

           
        ])]

if __name__ == '__main__':
    app.run_server(debug=True)
