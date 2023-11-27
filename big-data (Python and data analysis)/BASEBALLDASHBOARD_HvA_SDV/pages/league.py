# pylint: disable = line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import dash_table

from MySQL_data import SQL_Engine
from server import app

game_logs_batting_df = pd.read_sql_table('db_Batting_Gamelogs', SQL_Engine)
game_logs_batting_df = game_logs_batting_df.sort_values(['PlayerName', 'Year', 'Month', 'Day'],
                                                        ascending=[True, True, True, True])
game_logs_pitching_df = pd.read_sql_table('db_Pitching_Gamelogs', SQL_Engine)
game_logs_pitching_df = game_logs_pitching_df.sort_values(['PlayerName', 'Year', 'Month', 'Day'],
                                                          ascending=[True, True, True, True])


# Reading SQL-data & creating dataframe
def get_dataframe(selected_tab):
    if selected_tab == 'tab-1':
        return game_logs_batting_df
    elif selected_tab == 'tab-2':
        return game_logs_pitching_df


def get_position(selected_player):
    game_career_df = pd.read_sql_table('db_Batting_Career', SQL_Engine)
    game_career_df = game_career_df.loc[game_career_df['PlayerName'] == selected_player]
    game_career_df = game_career_df.loc[:, ['MainPos']].reset_index(drop=True)
    return game_career_df['MainPos'][0]


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# setting up page layout
layout = html.Div([
    html.Header([
        html.H1('Single Player', id='title'),
    ], className="header"),

    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Batting',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Pitching',
                value='tab-2',
                className='custom-tab',
                selected_className='custom-tab--selected'
            )
        ]),

    html.Div(id='tabs-content-classes'),

    html.Div([
                html.H3('Overview stats'),
            ], className='overview-stats-css'),

    html.Div(id='page-overview', className='player-selection-league')
])

order_leagues = [
    ' ',  # Do not Delete this line of code
    'MLB (USA)',
    'AAA-MEX',
    'AAA-PCL',
    'AAA-IL',
    'AA-SOUL',
    'AA-EL',
    'AA-TL',
    'A+-CARL',
    'A+-CALL',
    'A+-FLOR',
    'A-SALL',
    'A-MIDW',
    'A--NYPL',
    'A--NORW',
    'Rk-ARIZ',
    'Rk-PION',
    'Rk-APPY',
    'Rk-GULF',
    'FRk-DOSL',
    'FRk-VESL',
    'Fgn-AUBL',
    'FgW-VEWL',
    'FgW-DOWL',
    'FgW-MXPW',
    'Fal-AZFL',
    'Hoofdklasse Honkbal (NLD)'
]

batting_stats_type = [
    {'label': 'PA', 'value': 'pa'},
    {'label': 'AB', 'value': 'ab'},
    {'label': 'H', 'value': 'h'},
    {'label': 'HR', 'value': 'hr'},
    {'label': 'R', 'value': 'r'},
    {'label': 'RBI', 'value': 'rbi'},
    {'label': 'SB', 'value': 'sb'},
    {'label': 'CS', 'value': 'cs'},
    {'label': 'AVG', 'value': 'avg_value'},
    {'label': 'OBP', 'value': 'obp_value'},
    {'label': 'SLG', 'value': 'slg_value'},
    {'label': 'OPS', 'value': 'ops_value'},
    {'label': 'ISO', 'value': 'iso_value'}
]

pitching_stats_type = [
    {'label': 'GS', 'value': 'gs'},
    {'label': 'IP', 'value': 'ip_label'},
    {'label': 'H', 'value': 'h'},
    {'label': 'R', 'value': 'r'},
    {'label': 'BB', 'value': 'bb'},
    {'label': 'SO', 'value': 'so'},
    {'label': 'HBP', 'value': 'hbp'},
    {'label': 'IBB', 'value': 'ibb'},
    {'label': 'AB', 'value': 'ab'},
    {'label': 'BF', 'value': 'bf'},
    {'label': 'FO', 'value': 'fo'},
    {'label': 'GO', 'value': 'go'},
    {'label': 'Pit', 'value': 'np'}
]


def get_dataframe_with_filters(selected_player, selected_team, selected_year, selected_tab):
    game_logs_player = get_dataframe(selected_tab)
    if selected_team is None and selected_year is None:
        game_logs_player = game_logs_player.loc[game_logs_player['PlayerName'] == selected_player]
    elif selected_team is not None and selected_year is None:
        game_logs_player = game_logs_player.loc[game_logs_player['PlayerName'] == selected_player].loc[
            game_logs_player['Team'] == selected_team]
    elif selected_team is None and selected_year is not None:
        game_logs_player = game_logs_player.loc[game_logs_player['PlayerName'] == selected_player].loc[
            game_logs_player['Year'].isin(selected_year)]
    else:
        game_logs_player = game_logs_player.loc[game_logs_player['PlayerName'] == selected_player].loc[
            game_logs_player['Year'].isin(selected_year)].loc[
            game_logs_player['Team'] == selected_team]
    return game_logs_player


@app.callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'))
def render_content(tab):
    game_logs_df = get_dataframe(tab)
    if tab == 'tab-1':
        return html.Div([

            html.Div([
                html.H3('Player stats'),
            ], className='player-stats-css'),

            html.Div([
                html.Div([
                    html.Label("Select player name:", className='player-selection-league'),
                    dcc.Dropdown(
                        id='PlayerName1', className='player-selection-league-dropdown',
                        options=[{'label': i, 'value': i} for i in game_logs_df.PlayerName.unique()],
                        placeholder='Select a player')
                ], id='player-choices', className='player-dropdown-css'),

                html.Div([
                    html.Label("Select type:", className='player-selection-league'),
                    dcc.Dropdown(id='gant-type', multi=False, clearable=False,
                                 style={'color': 'black', 'cursor': 'default'},
                                 className='player-selection-league-dropdown',
                                 options=batting_stats_type, value='pa'),
                ], className='player-dropdown-css'),
                html.Div([
                    html.Label("Select team name:", className='player-selection-league'),
                    dcc.Dropdown(
                        id='team-choices-selected', className='player-selection-league-dropdown',
                        placeholder='Select a team')
                ], id='team-choices', className='player-dropdown-css'),

                html.Div([
                    html.Label("Select year:", className='player-selection-league'),
                    dcc.Dropdown(
                        id='year-type-selected', className='player-selection-league-dropdown',
                        placeholder='Select a year', multi=True)
                ], id='year-choices', className='player-dropdown-css'),

            ], className='row'),

            html.Div([], id='gant-visualization', className='gant-visualization-overview'),
            dcc.Graph(id='league_graph')
        ])
    elif tab == 'tab-2':
        return html.Div([

            html.Div([
                html.H3('Player stats'),
            ], className='player-stats-css'),

            html.Div([
                html.Div([
                    html.Label("Select player name:", className='player-selection-league'),
                    dcc.Dropdown(
                        id='PlayerName1', className='player-selection-league-dropdown',
                        options=[{'label': i, 'value': i} for i in game_logs_df.PlayerName.unique()],
                        placeholder='Select a player')
                ], id='player-choices', className='player-dropdown-css'),

                html.Div([
                    html.Label("Select type:", className='player-selection-league'),
                    dcc.Dropdown(id='gant-type', multi=False, clearable=False,
                                 style={'color': 'black', 'cursor': 'default'},
                                 className='player-selection-league-dropdown',
                                 options=pitching_stats_type, value='gs'),
                ], className='player-dropdown-css'),

                html.Div([
                    html.Label("Select team name:", className='player-selection-league'),
                    dcc.Dropdown(
                        id='team-choices-selected', className='player-selection-league-dropdown',
                        placeholder='Select a team')
                ], id='team-choices', className='player-dropdown-css'),

                html.Div([
                    html.Label("Select year:", className='player-selection-league'),
                    dcc.Dropdown(
                        id='year-type-selected', className='player-selection-league-dropdown',
                        placeholder='Select a year', multi=True)
                ], id='year-choices', className='player-dropdown-css'),
            ], className='row'),
            html.Div([], id='gant-visualization', className='gant-visualization-overview'),
            dcc.Graph(id='league_graph')
        ])


# creating & returning graphs
@app.callback(
    Output('league_graph', 'figure'),
    [Input('PlayerName1', 'value'),
     Input('team-choices-selected', 'value'),
     Input('year-type-selected', 'value'),
     Input('tabs-with-classes', 'value')]
)
def update_player(selected_player, selected_team, selected_year, selected_tab):
    game_logs_player = get_dataframe_with_filters(selected_player, selected_team, selected_year, selected_tab)
    selected_player = game_logs_player[
        ~game_logs_player[['PlayerName', 'Year', 'Month']].apply(frozenset, axis=1).duplicated()]
    fig = px.line(selected_player,
                  x='DateString',
                  y='League',
                  title='Played leagues:',
                  category_orders={'League': order_leagues},
                  labels={'DateString': 'Date'},
                  height=600
                  )
    return fig


@app.callback(Output('gant-visualization', 'children'),
              [Input('PlayerName1', 'value'),
               Input('gant-type', 'value'),
               Input('team-choices-selected', 'value'),
               Input('year-type-selected', 'value'),
               Input('tabs-with-classes', 'value')])
def get_gant_visualization(selected_player, gant_type, selected_team, selected_year, selected_tab):
    if selected_player is None:
        return html.Label("No player selected to show stats", className='player-selection-league')
    game_logs_player = get_dataframe_with_filters(selected_player, selected_team, selected_year, selected_tab)
    selected_player_df = game_logs_player[
        ~game_logs_player[['PlayerName', 'Year', 'Month']].apply(frozenset, axis=1).duplicated()]
    selected_player_df = selected_player_df.groupby(['PlayerName', 'Year'])[gant_type].sum().reset_index()
    selected_player_df['Year'] = pd.to_datetime(selected_player_df['Year'], format='%Y')
    fig = px.bar(selected_player_df, y="Year", x='{}'.format(gant_type), orientation='h',
                 title='Selected type: {0}'.format(gant_type))
    fig.update_layout(yaxis={'tickformat': '%Y', 'nticks': selected_player_df.shape[0]})
    return html.Div(
        [
            dcc.Graph(figure=fig)
        ], className=""
    )


@app.callback(Output('team-choices-selected', 'options'),
              [Input('PlayerName1', 'value'),
               Input('tabs-with-classes', 'value')])
def update_team_dropdown_options(selected_player, selected_tab):
    if selected_player is None:
        return []
    game_logs_player = get_dataframe(selected_tab)

    game_logs_player = game_logs_player.loc[game_logs_player['PlayerName'] == selected_player]
    return [{'label': i, 'value': i} for i in game_logs_player.Team.unique()]


@app.callback(Output('year-type-selected', 'options'),
              [Input('PlayerName1', 'value'),
               Input('tabs-with-classes', 'value')])
def update_year_dropdown_options(selected_player, selected_tab):
    if selected_player is None:
        return []
    game_logs_player = get_dataframe(selected_tab)

    game_logs_player = game_logs_player.loc[game_logs_player['PlayerName'] == selected_player]
    return [{'label': i, 'value': i} for i in game_logs_player.Year.unique()]


@app.callback(Output('page-overview', 'children'),
              [Input('PlayerName1', 'value')])
def intra_page_content_overview(selected_player):
    if selected_player is None:
        return html.Label("No player selected to show stats")
    position = get_position(selected_player)

    dfBattingOverview = pd.read_sql_table('db_Batting_Summary', SQL_Engine)
    dfFieldingOverview = pd.read_sql_table('db_Fielding_Summary', SQL_Engine)
    dfBattingOverview = dfBattingOverview.loc[dfBattingOverview['PlayerName'] == selected_player]
    dfFieldingOverview = dfFieldingOverview.loc[dfFieldingOverview['PlayerName'] == selected_player]

    dfBattingOverview = dfBattingOverview.loc[:,
                        ['Year', 'Team', 'League', 'g', 'pa', 'ab', 'h', 'hr', 'r', 'rbi', 'sb', 'cs', 'avg_label',
                         'obp_label', 'slg_label', 'ops_label', 'iso_label']]
    dfBattingOverview.columns = ['Year', 'Team', 'League', 'G', 'PA', 'AB', 'H', 'HR', 'R', 'RBI', 'SB', 'CS',
                                 'AVG', 'OBP', 'SLG', 'OPS', 'ISO']

    dfFieldingOverview = dfFieldingOverview.loc[:, ['Year', 'Team', 'League', 'g', 'po', 'a', 'e', 'ch', 'favg_label']]
    dfFieldingOverview.columns = ['Year', 'Team', 'League', 'G', 'PO', 'A', 'E', 'CH', 'FLD%']

    if position != 'Pitcher':

        return html.Div([

            html.Div([
                html.H4(['Batting overview'], className='table-title', style={'margin-top': '0'}),
                html.Div([
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in dfBattingOverview.columns],
                        data=dfBattingOverview.to_dict('records'),
                        style_cell={'minWidth': 30, 'whiteSpace': 'normal'},
                        style_cell_conditional=[
                            {
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['Name', 'League', 'Main Position', 'Team']
                        ],
                        sort_action="native",
                    )
                ], id='batting-overview-table', className='overview-table')
            ], id='batting-overview', className='batting-overview'),

            html.Div([
                html.H4(['Fielding overview'], className='table-title'),
                html.Div([
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in dfFieldingOverview.columns],
                        data=dfFieldingOverview.to_dict('records'),
                        style_cell={'minWidth': 30, 'whiteSpace': 'normal'},
                        style_cell_conditional=[
                            {
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['Name', 'League', 'Main Position', 'Team']
                        ],
                        sort_action="native",
                    )
                ], id='fielding-overview-table', className='overview-table')
            ], id='fielding-overview', className='fielding-overview'),
        ])

    else:
        dfPitchingOverview = pd.read_sql_table('db_Pitching_Summary', SQL_Engine)
        dfPitchingOverview = dfPitchingOverview.loc[dfPitchingOverview['PlayerName'] == selected_player]
        dfPitchingOverview = dfPitchingOverview.loc[:,
                             ['Year', 'Team', 'League', 'g', 'ip_label', 'h', 'r', 'er', 'bb', 'so', 'hbp', 'ibb', 'ab',
                              'bf', 'fo', 'go', 'np', 'Win', 'Loss', 'Save', 'era_label', 'wlp_label', 'whip_label',
                              'h9_label', 'bb9_label', 'so9_label', 'sobb_label']]
        dfPitchingOverview.columns = ['Year', 'Team', 'League', 'G', 'IP', 'H', 'R', 'ER', 'BB', 'SO', 'HBP',
                                      'IBB', 'AB', 'BF', 'FO', 'GO', 'Pit', 'Win', 'Loss', 'Save', 'ERA', 'WLP',
                                      'WHIP', 'H9', 'BB9', 'SO9', 'SOBB']
        return html.Div([

            html.Div([
                html.H4(['Pitching overview'], className='table-title', style={'margin-top': '0'}),
                html.Div([
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in dfPitchingOverview.columns],
                        data=dfPitchingOverview.to_dict('records'),
                        style_cell={'minWidth': 30, 'whiteSpace': 'normal'},
                        style_cell_conditional=[
                            {
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['Name', 'League', 'Main Position', 'Team']
                        ],
                        sort_action="native",
                    )
                ], id='pitching-overview-table', className='overview-table')
            ], id='pitching-overview', className='pitching-overview'),

            html.Div([
                html.H4(['Batting overview'], className='table-title'),
                html.Div([
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in dfBattingOverview.columns],
                        data=dfBattingOverview.to_dict('records'),
                        style_cell={'minWidth': 30, 'whiteSpace': 'normal'},
                        style_cell_conditional=[
                            {
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['Name', 'League', 'Main Position', 'Team']
                        ],
                        sort_action="native",
                    )
                ], id='batting-overview-table', className='overview-table')
            ], id='batting-overview', className='batting-overview'),

            html.Div([
                html.H4(['Fielding overview'], className='table-title'),
                html.Div([
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in dfFieldingOverview.columns],
                        data=dfFieldingOverview.to_dict('records'),
                        style_cell={'minWidth': 30, 'whiteSpace': 'normal'},
                        style_cell_conditional=[
                            {
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['Name', 'League', 'Main Position', 'Team']
                        ],
                        sort_action="native",
                    )
                ], id='fielding-overview-table', className='overview-table')
            ], id='fielding-overview', className='fielding-overview'),
        ])


@app.callback(Output('gant-type', 'value'), [Input('tabs-with-classes', 'value')])
def clear_selected_type(selected_tab):
    if selected_tab == 'tab-1':
        return 'pa'
    elif selected_tab == 'tab-2':
        return 'gs'


@app.callback(Output('team-choices-selected', 'value'), [Input('PlayerName1', 'value')])
def clear_selected_team(select_player):
    if select_player is not None or select_player == '':
        return None


@app.callback(Output('year-type-selected', 'value'), [Input('PlayerName1', 'value')])
def clear_selected_year(select_player):
    if select_player is not None or select_player == '':
        return None
