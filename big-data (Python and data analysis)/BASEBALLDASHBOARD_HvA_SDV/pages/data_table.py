#pylint: disable = line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order
import plotly.graph_objects as go
import pandas as pd
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
from pandas import DataFrame, read_sql, read_csv, concat

from server import app

app.css.config.serve_locally = True

PositionList = ['Pos_1b', 'Pos_2b', 'Pos_3b', 'Pos_c', 'Pos_cf', 'Pos_dh', 'Pos_lf', 'Pos_p', 'Pos_ph', 'Pos_pr', 'Pos_rf', 'Pos_ss']
PositionDict = {'Pos_1b': '1B', 'Pos_2b': '2B', 'Pos_3b': '3B', 'Pos_ss': 'SS', 'Pos_lf': 'LF', 'Pos_cf': 'CF', 'Pos_rf': 'RF', 'Pos_p': 'P', 'Pos_c': 'C', 'Pos_dh': 'DH', 'Pos_ph': 'PH', 'Pos_pr': 'PR'}


layout = html.Div([
    # Nav bar
    html.Header([
        html.H1('Data Table', id='title')
    ], className='header'),

    html.Div([
        html.P([
            dbc.Col(html.H4("Select all the variables for the table", className="data-table-titel")
                    , className="mb-5 mt-5")
        ]),

            
        # html.Button(['Show / hide filters'], id='dropdown-button', n_clicks=0),
        html.Div([

            html.Div([
                html.P(['Type:']),
                dcc.Dropdown(id='filter-type', placeholder='--All--', multi=False,
                            options=[
                                {'label': 'Batting', 'value': 'Batting'},
                                {'label': 'Pitching', 'value': 'Pitching'},
                                {'label': 'Fielding', 'value': 'Fielding'}],
                            value='Batting',
                            clearable=False),
            ], id='group-type', className='data-table-knoppen'),

            html.Div([
                html.P(['Time interval:']),
                dcc.Dropdown(id='filter-interval', placeholder='--All--', multi=False,
                            options=[
                                {'label': 'Game logs', 'value': 'Gamelogs'},
                                {'label': 'Summary', 'value': 'Summary'},
                                {'label': 'Yearly', 'value': 'Yearly'},
                                {'label': 'Career', 'value': 'Career'}],
                            value='Gamelogs',
                            clearable=False),
            ], id='group-interval', className='data-table-knoppen'),



            html.Div([
                html.P(['League:']),
                dcc.Dropdown(id='groupby-league', placeholder='--All--', multi=True),
            ], id='group-league', className='data-table-knoppen'),

            html.Div([
                html.P(['Position:']),
                dcc.Dropdown(id='groupby-position', placeholder='--All--', multi=True),
            ], id='group-position', style={'color': 'black', 'cursor': 'default', 'width': '150px', 'display': 'inline-block', 'margin-right': '20px'}),
            
            html.Div([
                html.P(['Team:']),
                dcc.Dropdown(id='groupby-team', placeholder='--All--', multi=True),
            ], id='group-team', className='data-table-knoppen'),
            
            html.Div([
                html.P(['Player:']),
                dcc.Dropdown(id='groupby-player', placeholder='--All--', multi=True),
            ], id='group-player', className='data-table-knoppen'),

            html.Div([
                html.P(['Season:']),
                dcc.Dropdown(id='filter-years', placeholder='--All--', multi=True),
            ], id='group-years', className='data-table-knoppen'),

            html.Div([
                html.P(['Seasontype:']),
                dcc.Dropdown(id='filter-seasontype', placeholder='--All--', multi=False),
            ], id='group-seasontype', className='data-table-knoppen'),

        ], id='dropdown-content', style={'max-width': '1410px'}),

        html.Button(['Load table'], id='load-table', n_clicks=0, className='data-table-button'),



        html.Div(id='empty-div'),
        
    ], className='dropdown-div', style={'display': 'inline-block'}),

    html.Div([
        html.Div(id='table1')
    ], className='data-table'),
],)


@app.callback(Output('dropdown-content', 'className'),
             [Input('dropdown-button', 'n_clicks')])
def show_dropdown_filters(n_clicks):
    if n_clicks % 2 != 1:
        return 'dropdown-content-visible'
    else:
        return 'dropdown-content-hidden'


@app.callback(Output('groupby-league', 'options'),
              [Input('filter-type', 'value'),
               Input('filter-interval', 'value')])
def update_groupby_league(type, interval):
    if interval != 'Career':
        groupby_league = read_sql(("""SELECT DISTINCT League FROM db_""" + type + """_""" + interval), SQL_Engine)
        groupby_league = groupby_league['League'].tolist()
        groupby_league.sort()

        options = [{'label': i, 'value': ("'" + i + "'")} for i in groupby_league]
        return options
    else: 
        return []


@app.callback(Output('groupby-position', 'options'),
              [Input('filter-type', 'value')])
def update_groupby_position(type):
    if type != 'Pitching':
        options=[
            {'label': '1B', 'value': 'Pos_1b'},
            {'label': '2B', 'value': 'Pos_2b'},
            {'label': '3B', 'value': 'Pos_3b'},
            {'label': 'SS', 'value': 'Pos_ss'},
            {'label': 'LF', 'value': 'Pos_lf'},
            {'label': 'CF', 'value': 'Pos_cf'},
            {'label': 'RF', 'value': 'Pos_rf'},
            {'label': 'P', 'value': 'Pos_p'},
            {'label': 'C', 'value': 'Pos_c'},
            {'label': 'DH', 'value': 'Pos_dh'},
            {'label': 'PH', 'value': 'Pos_ph'},
            {'label': 'PR', 'value': 'Pos_pr'},
        ]
        return options
    else: 
        return []


@app.callback(Output('groupby-team', 'options'),
              [Input('groupby-league', 'value'),
               Input('groupby-player', 'value'),
               Input('filter-type', 'value'),
               Input('filter-interval', 'value')])
def update_groupby_team(groupby_league, groupby_player, type, interval):
    if interval != 'Career' and interval != 'Yearly':
        SQLStatement = """SELECT DISTINCT Team FROM db_""" + type + """_""" + interval
        SQLParameter = ""

        if groupby_league != None:
            if len(groupby_league) == 1:
                SQLParameter = " WHERE (League = " + groupby_league[0] + ")"
            else:
                for league in groupby_league:
                    if SQLParameter == "":
                        SQLParameter = " WHERE (League = " + league
                    elif league != groupby_league[-1]:
                        SQLParameter = SQLParameter + " OR League = " + league
                    elif league == groupby_league[-1]:
                        SQLParameter = SQLParameter + " OR League = " + league + ")"

        if groupby_player != None:
            if len(groupby_player) == 1:
                if SQLParameter == "":
                    SQLParameter = " WHERE (PlayerName = " + groupby_player[0] + ")"
                else:
                    SQLParameter = SQLParameter + " AND (PlayerName = " + groupby_player[0] + ")"
            else:
                for player in groupby_player:
                    if SQLParameter == "":
                        SQLParameter = " WHERE (PlayerName = " + player
                    elif SQLParameter != "" and player == groupby_player[0]:
                        SQLParameter = SQLParameter + " AND (PlayerName = " + player
                    elif player != groupby_player[0] and player != groupby_player[-1]:
                        SQLParameter = SQLParameter + " OR PlayerName = " + player
                    elif player == groupby_player[-1]:
                        SQLParameter = SQLParameter + " OR PlayerName = " + player + ")"

        
        load_command = SQLStatement + SQLParameter

        groupby_team = read_sql(load_command, SQL_Engine)
        groupby_team = groupby_team['Team'].tolist()
        groupby_team.sort()

        options = [{'label': i, 'value': ("'" + i + "'")} for i in groupby_team]
        return options
    else:
        return []     


@app.callback(Output('groupby-player', 'options'),
              [Input('groupby-league', 'value'),
               Input('groupby-position', 'value'),
               Input('groupby-team', 'value'),
               Input('filter-years', 'value'),
               Input('filter-type', 'value'),
               Input('filter-interval', 'value')])
def update_groupby_player(groupby_league, groupby_position, groupby_team, filter_year, type, interval):
    SQLStatement = """SELECT DISTINCT PlayerName FROM db_""" + type + """_""" + interval
    SQLParameter = ""

    if groupby_league != None:
        if len(groupby_league) == 1:
            SQLParameter = " WHERE (League = " + groupby_league[0] + ")"
        else:
            for league in groupby_league:
                if SQLParameter == "":
                    SQLParameter = " WHERE (League = " + league
                elif league != groupby_league[-1]:
                    SQLParameter = SQLParameter + " OR League = " + league
                elif league == groupby_league[-1]:
                    SQLParameter = SQLParameter + " OR League = " + league + ")"

    if groupby_position != None:
        if len(groupby_position) == 1:
            if SQLParameter == "":
                SQLParameter = " WHERE (" + groupby_position[0] + " = 1)"
            else:
                SQLParameter = SQLParameter + " AND (" + groupby_position[0] + " = 1)"
        else:
            for position in groupby_position:
                if SQLParameter == "":
                    SQLParameter = " WHERE (" + position + " = 1"
                elif SQLParameter != "" and position == groupby_position[0]:
                    SQLParameter = SQLParameter + " AND (" + position + " = 1"
                elif position != groupby_position[0] and position != groupby_position[-1]:
                    SQLParameter = SQLParameter + " OR " + position + " = 1"
                elif position == groupby_position[-1]:
                    SQLParameter = SQLParameter + " OR " + position + " = 1)"

    if groupby_team != None:
        if len(groupby_team) == 1:
            if SQLParameter == "":
                SQLParameter = " WHERE (Team = " + groupby_team[0] + ")"
            else:
                SQLParameter = SQLParameter + " AND (Team = " + groupby_team[0] + ")"
        else:
            for team in groupby_team:
                if SQLParameter == "":
                    SQLParameter = " WHERE (Team = " + team
                elif SQLParameter != "" and team == groupby_team[0]:
                    SQLParameter = SQLParameter + " AND (Team = " + team
                elif team != groupby_team[0] and team != groupby_team[-1]:
                    SQLParameter = SQLParameter + " OR Team = " + team
                elif team == groupby_team[-1]:
                    SQLParameter = SQLParameter + " OR Team = " + team + ")"

    if filter_year != None:
        if len(filter_year) == 1:
            if SQLParameter == "":
                SQLParameter = " WHERE (Year = " + filter_year[0] + ")"
            else:
                SQLParameter = SQLParameter + " AND (Year = " + filter_year[0] + ")"
        else:
            for year in filter_year:
                if SQLParameter == "":
                    SQLParameter = " WHERE (Year = " + year
                elif SQLParameter != "" and year == filter_year[0]:
                    SQLParameter = SQLParameter + " AND (Year = " + year
                elif year != filter_year[0] and year != filter_year[-1]:
                    SQLParameter = SQLParameter + " OR Year = " + year
                elif year == filter_year[-1]:
                    SQLParameter = SQLParameter + " OR Year = " + year + ")"

    
    load_command = SQLStatement + SQLParameter

    groupby_player = read_sql(load_command, SQL_Engine)
    groupby_player = groupby_player['PlayerName'].tolist()
    groupby_player.sort()

    options = [{'label': i, 'value': ("'" + i + "'")} for i in groupby_player]
    return options


@app.callback(Output('filter-years', 'options'),
              [Input('groupby-league', 'value'),
               Input('groupby-position', 'value'),
               Input('groupby-team', 'value'),
               Input('groupby-player', 'value'),
               Input('filter-type', 'value'),
               Input('filter-interval', 'value')])
def update_years(groupby_league, groupby_position, groupby_team, groupby_player, type, interval):
    if interval != 'Career':
        SQLStatement = """SELECT DISTINCT Year FROM db_""" + type + """_""" + interval
        SQLParameter = ""

        if groupby_league != None:
            if len(groupby_league) == 1:
                SQLParameter = " WHERE (League = " + groupby_league[0] + ")"
            else:
                for league in groupby_league:
                    if SQLParameter == "":
                        SQLParameter = " WHERE (League = " + league
                    elif league != groupby_league[-1]:
                        SQLParameter = SQLParameter + " OR League = " + league
                    elif league == groupby_league[-1]:
                        SQLParameter = SQLParameter + " OR League = " + league + ")"

        if groupby_position != None:
            if len(groupby_position) == 1:
                if SQLParameter == "":
                    SQLParameter = " WHERE (" + groupby_position[0] + " = 1)"
                else:
                    SQLParameter = SQLParameter + " AND (" + groupby_position[0] + " = 1)"
            else:
                for position in groupby_position:
                    if SQLParameter == "":
                        SQLParameter = " WHERE (" + position + " = 1"
                    elif SQLParameter != "" and position == groupby_position[0]:
                        SQLParameter = SQLParameter + " AND (" + position + " = 1"
                    elif position != groupby_position[0] and position != groupby_position[-1]:
                        SQLParameter = SQLParameter + " OR " + position + " = 1"
                    elif position == groupby_position[-1]:
                        SQLParameter = SQLParameter + " OR " + position + " = 1)"

        if groupby_team != None:
            if len(groupby_team) == 1:
                if SQLParameter == "":
                    SQLParameter = " WHERE (Team = " + groupby_team[0] + ")"
                else:
                    SQLParameter = SQLParameter + " AND (Team = " + groupby_team[0] + ")"
            else:
                for team in groupby_team:
                    if SQLParameter == "":
                        SQLParameter = " WHERE (Team = " + team
                    elif SQLParameter != "" and team == groupby_team[0]:
                        SQLParameter = SQLParameter + " AND (Team = " + team
                    elif team != groupby_team[0] and team != groupby_team[-1]:
                        SQLParameter = SQLParameter + " OR Team = " + team
                    elif team == groupby_team[-1]:
                        SQLParameter = SQLParameter + " OR Team = " + team + ")"

        if groupby_player != None:
            if len(groupby_player) == 1:
                if SQLParameter == "":
                    SQLParameter = " WHERE (PlayerName = " + groupby_player[0] + ")"
                else:
                    SQLParameter = SQLParameter + " AND (PlayerName = " + groupby_player[0] + ")"
            else:
                for player in groupby_player:
                    if SQLParameter == "":
                        SQLParameter = " WHERE (PlayerName = " + player
                    elif SQLParameter != "" and player == groupby_player[0]:
                        SQLParameter = SQLParameter + " AND (PlayerName = " + player
                    elif player != groupby_player[0] and player != groupby_player[-1]:
                        SQLParameter = SQLParameter + " OR PlayerName = " + player
                    elif player == groupby_player[-1]:
                        SQLParameter = SQLParameter + " OR PlayerName = " + player + ")"

        
        load_command = SQLStatement + SQLParameter
        
        filter_year = read_sql(load_command, SQL_Engine)
        filter_year = filter_year['Year'].tolist()
        filter_year.sort(reverse=True)

        options = [{'label': str(i), 'value': ("'" + str(i) + "'")} for i in filter_year]
        return options
    else:
        return []


@app.callback(Output('filter-seasontype', 'options'),
              [Input('filter-interval', 'value')])
def update_filter_seasontype(interval):
    if interval == 'Gamelogs':
        options=[
            {'label': 'Regular Season', 'value': "'Regular Season'"},
            {'label': 'Post-Season', 'value': "'Post-Season'"},
        ]
        return options
    else: 
        return []


@app.callback([Output('table1', 'children'),
               Output('table1', 'className')],
              [Input('load-table', 'n_clicks')],
              [State('groupby-league', 'value'),
               State('groupby-position', 'value'),
               State('groupby-team', 'value'),
               State('groupby-player', 'value'),
               State('filter-years', 'value'),
               State('filter-type', 'value'),
               State('filter-interval', 'value'),
               State('filter-seasontype', 'value')])
def update_table1(n_clicks, groupby_league, groupby_position, groupby_team, groupby_player, filter_year, type, interval, filter_seasontype):
    if n_clicks > 0:
        SQLStatement = """SELECT * FROM db_""" + type + """_""" + interval
        SQLParameter = ""

        if groupby_league != None:
            if len(groupby_league) == 1:
                SQLParameter = " WHERE (League = " + groupby_league[0] + ")"
            else:
                for league in groupby_league:
                    if SQLParameter == "":
                        SQLParameter = " WHERE (League = " + league
                    elif league != groupby_league[-1]:
                        SQLParameter = SQLParameter + " OR League = " + league
                    elif league == groupby_league[-1]:
                        SQLParameter = SQLParameter + " OR League = " + league + ")"

        if groupby_position != None:
            if len(groupby_position) == 1:
                if SQLParameter == "":
                    SQLParameter = " WHERE (" + groupby_position[0] + " = 1)"
                else:
                    SQLParameter = SQLParameter + " AND (" + groupby_position[0] + " = 1)"
            else:
                for position in groupby_position:
                    if SQLParameter == "":
                        SQLParameter = " WHERE (" + position + " = 1"
                    elif SQLParameter != "" and position == groupby_position[0]:
                        SQLParameter = SQLParameter + " AND (" + position + " = 1"
                    elif position != groupby_position[0] and position != groupby_position[-1]:
                        SQLParameter = SQLParameter + " OR " + position + " = 1"
                    elif position == groupby_position[-1]:
                        SQLParameter = SQLParameter + " OR " + position + " = 1)"

        if groupby_team != None:
            if len(groupby_team) == 1:
                if SQLParameter == "":
                    SQLParameter = " WHERE (Team = " + groupby_team[0] + ")"
                else:
                    SQLParameter = SQLParameter + " AND (Team = " + groupby_team[0] + ")"
            else:
                for team in groupby_team:
                    if SQLParameter == "":
                        SQLParameter = " WHERE (Team = " + team
                    elif SQLParameter != "" and team == groupby_team[0]:
                        SQLParameter = SQLParameter + " AND (Team = " + team
                    elif team != groupby_team[0] and team != groupby_team[-1]:
                        SQLParameter = SQLParameter + " OR Team = " + team
                    elif team == groupby_team[-1]:
                        SQLParameter = SQLParameter + " OR Team = " + team + ")"

        if groupby_player != None:
            if len(groupby_player) == 1:
                if SQLParameter == "":
                    SQLParameter = " WHERE (PlayerName = " + groupby_player[0] + ")"
                else:
                    SQLParameter = SQLParameter + " AND (PlayerName = " + groupby_player[0] + ")"
            else:
                for player in groupby_player:
                    if SQLParameter == "":
                        SQLParameter = " WHERE (PlayerName = " + player
                    elif SQLParameter != "" and player == groupby_player[0]:
                        SQLParameter = SQLParameter + " AND (PlayerName = " + player
                    elif player != groupby_player[0] and player != groupby_player[-1]:
                        SQLParameter = SQLParameter + " OR PlayerName = " + player
                    elif player == groupby_player[-1]:
                        SQLParameter = SQLParameter + " OR PlayerName = " + player + ")"

        if filter_year != None:
            if len(filter_year) == 1:
                if SQLParameter == "":
                    SQLParameter = " WHERE (Year = " + filter_year[0] + ")"
                else:
                    SQLParameter = SQLParameter + " AND (Year = " + filter_year[0] + ")"
            else:
                for year in filter_year:
                    if SQLParameter == "":
                        SQLParameter = " WHERE (Year = " + year
                    elif SQLParameter != "" and year == filter_year[0]:
                        SQLParameter = SQLParameter + " AND (Year = " + year
                    elif year != filter_year[0] and year != filter_year[-1]:
                        SQLParameter = SQLParameter + " OR Year = " + year
                    elif year == filter_year[-1]:
                        SQLParameter = SQLParameter + " OR Year = " + year + ")"
        
        if filter_seasontype != None:
            if SQLParameter == "":
                SQLParameter = " WHERE SeasonType = " + filter_seasontype
            else:
                SQLParameter = SQLParameter + " AND SeasonType = " + filter_seasontype


        load_command = SQLStatement + SQLParameter + " LIMIT 200"
        
        df = read_sql(load_command, SQL_Engine)
        SortList = ['PlayerName']

        if 'Year' in df.columns:
            SortList.append('Year')
        
        if 'Team' in df.columns:
            SortList.append('Team')
        
        df = df.sort_values(SortList, ascending=[True for i in SortList])
        
        dfCols = []
        for i in range(len(df.columns)):
            if '_value' not in df.columns[i] and 'Pos_' not in df.columns[i]:
                dfCols.append(df.columns[i])

        df = df[dfCols]

        if 'PlayerName' in df.columns: 
            df.rename(columns={'PlayerName': 'Player'},inplace = True)

        if 'SeasonType' in df.columns: 
            df.rename(columns={'SeasonType': 'Season Type'},inplace = True)

        if 'HomeGame' in df.columns: 
            for i in range(len(df['HomeGame'])):
                if df['HomeGame'][i] == 0:
                    df['HomeGame'][i] = 'Away'
                else:
                    df['HomeGame'][i] = 'Home'
            df.rename(columns={'HomeGame': 'Home/Away'},inplace = True)

        if 'DateString' in df.columns: 
            df.rename(columns={'DateString': 'Date'},inplace = True)
            df = df.drop(columns=['Year', 'Month', 'Day'])

        if 'MatchID' in df.columns: 
            df = df.drop(columns=['MatchID'])

        if 'g' in df.columns: 
            df.rename(columns={'g': 'G'},inplace = True)

        if 'pa' in df.columns: 
            df.rename(columns={'pa': 'PA'},inplace = True)

        if 'ab' in df.columns: 
            df.rename(columns={'ab': 'AB'},inplace = True)

        if 'r' in df.columns: 
            df.rename(columns={'r': 'R'},inplace = True)

        if 'h' in df.columns: 
            df.rename(columns={'h': 'H'},inplace = True)

        if 'rbi' in df.columns: 
            df.rename(columns={'rbi': 'RBI'},inplace = True)

        if '2b' in df.columns: 
            df.rename(columns={'2b': '2B'},inplace = True)

        if '3b' in df.columns: 
            df.rename(columns={'3b': '3B'},inplace = True)

        if 'hr' in df.columns: 
            df.rename(columns={'hr': 'HR'},inplace = True)

        if 'bb' in df.columns: 
            df.rename(columns={'bb': 'BB'},inplace = True)

        if 'sb' in df.columns: 
            df.rename(columns={'sb': 'SB'},inplace = True)

        if 'cs' in df.columns: 
            df.rename(columns={'cs': 'CS'},inplace = True)

        if 'hbp' in df.columns: 
            df.rename(columns={'hbp': 'HBP'},inplace = True)

        if 'sh' in df.columns: 
            df.rename(columns={'sh': 'SH'},inplace = True)

        if 'sf' in df.columns: 
            df.rename(columns={'sf': 'SF'},inplace = True)

        if 'so' in df.columns: 
            df.rename(columns={'so': 'SO'},inplace = True)

        if 'ibb' in df.columns: 
            df.rename(columns={'ibb': 'IBB'},inplace = True)

        if 'gdp' in df.columns: 
            df.rename(columns={'gdp': 'GDP'},inplace = True)

        if 'MainPos' in df.columns: 
            df.rename(columns={'MainPos': 'Main pos.'},inplace = True)
            df = concat([df.drop(columns=['Main pos.']), df[['Main pos.']]], axis=1)

        if 'PosString' in df.columns: 
            df.rename(columns={'PosString': 'Pos'},inplace = True)
            df = concat([df.drop(columns=['Pos']), df[['Pos']]], axis=1)

        if 'avg_label' in df.columns: 
            df.rename(columns={'avg_label': 'AVG'},inplace = True)

        if 'obp_label' in df.columns: 
            df.rename(columns={'obp_label': 'OBP'},inplace = True)

        if 'slg_label' in df.columns: 
            df.rename(columns={'slg_label': 'SLG'},inplace = True)

        if 'ops_label' in df.columns: 
            df.rename(columns={'ops_label': 'OPS'},inplace = True)

        if 'iso_label' in df.columns: 
            df.rename(columns={'iso_label': 'ISO'},inplace = True)

        if 'gs' in df.columns: 
            df.rename(columns={'gs': 'GS'},inplace = True)

        if 'ip_label' in df.columns: 
            df.rename(columns={'ip_label': 'IP'},inplace = True)
        
        if 'Win' in df.columns and 'Loss' in df.columns and 'Save' in df.columns:
            df.insert(df.columns.get_loc('Win'), 'Dec', '')
            for i in range(len(df['Win'])):
                if df['Win'][i] == 1:
                    df['Dec'][i] = 'W'
                elif df['Loss'][i] == 1:
                    df['Dec'][i] = 'L'
                elif df['Save'][i] == 1:
                    df['Dec'][i] = 'S'
                else:
                    df['Dec'][i] = ''
            df = df.drop(columns=['Win', 'Loss', 'Save'])

        if 'er' in df.columns: 
            df.rename(columns={'er': 'ER'},inplace = True)

        if 'bf' in df.columns: 
            df.rename(columns={'bf': 'BF'},inplace = True)

        if 'fo' in df.columns: 
            df.rename(columns={'fo': 'FO'},inplace = True)

        if 'go' in df.columns: 
            df.rename(columns={'go': 'GO'},inplace = True)

        if 'np' in df.columns: 
            df.rename(columns={'np': 'Pit'},inplace = True)

        if 'era_label' in df.columns: 
            df.rename(columns={'era_label': 'ERA'},inplace = True)

        if 'wlp_label' in df.columns: 
            df.rename(columns={'wlp_label': 'WLP'},inplace = True)

        if 'whip_label' in df.columns: 
            df.rename(columns={'whip_label': 'WHIP'},inplace = True)

        if 'h9_label' in df.columns: 
            df.rename(columns={'h9_label': 'H9'},inplace = True)

        if 'bb9_label' in df.columns: 
            df.rename(columns={'bb9_label': 'BB9'},inplace = True)

        if 'so9_label' in df.columns: 
            df.rename(columns={'so9_label': 'SO9'},inplace = True)

        if 'sobb_label' in df.columns: 
            df.rename(columns={'sobb_label': 'SOBB'},inplace = True)

        if 'po' in df.columns: 
            df.rename(columns={'po': 'PO'},inplace = True)

        if 'a' in df.columns: 
            df.rename(columns={'a': 'A'},inplace = True)

        if 'e' in df.columns: 
            df.rename(columns={'e': 'E'},inplace = True)
        
        if 'ch' in df.columns: 
            df.rename(columns={'ch': 'CH'},inplace = True)

        if 'favg_label' in df.columns: 
            df.rename(columns={'favg_label': 'FLD%'},inplace = True)


        if 'FirstAppearance' in df.columns: 
            df = df.drop(columns=['FirstAppearance'])

        if 'LatestAppearance' in df.columns: 
            df = df.drop(columns=['LatestAppearance'])
        
        df.insert(0, 'Rows', 0)
        df['Rows'] = df.index + 1

        return [html.Table(
                [html.Thead([html.Tr([html.Th(col) for col in df.columns]) ], className='tabel-buiten') ] +
                [html.Tbody([html.Tr([html.Td(df.iloc[i][col], className='tabel-binnen') for col in df.columns], className='tabel-buiten') for i in range(len(df))], className='tabel-buiten') ]
            , className=str(type).lower()), str(interval).lower()]
    
    else:
        return ['', '']

