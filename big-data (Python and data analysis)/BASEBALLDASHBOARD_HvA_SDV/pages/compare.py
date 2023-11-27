#pylint: disable = line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pathlib
from server import app
from MySQL_data import SQL_Engine, execute_command, load_SQL_table


#load datasets
df_batting_career = pd.read_sql_table('db_Batting_Career', SQL_Engine)
df_batting_yearly = pd.read_sql_table('db_Batting_Yearly', SQL_Engine)
df_pitching_career = pd.read_sql_table('db_Pitching_Career', SQL_Engine)
df_pitching_yearly = pd.read_sql_table('db_Pitching_Yearly', SQL_Engine)

#drop _value columns and remove _label suffic
df_batting_career = df_batting_career.drop(columns=df_batting_career.columns[df_batting_career.columns.str.contains('value')])
df_batting_career.columns = df_batting_career.columns.str.replace('_label', '')
df_batting_yearly = df_batting_yearly.drop(columns=df_batting_yearly.columns[df_batting_yearly.columns.str.contains('value')])
df_batting_yearly.columns = df_batting_yearly.columns.str.replace('_label', '')
df_pitching_career = df_pitching_career.drop(columns=df_pitching_career.columns[df_pitching_career.columns.str.contains('value')])
df_pitching_career.columns = df_pitching_career.columns.str.replace('_label', '')
df_pitching_yearly = df_pitching_yearly.drop(columns=df_pitching_yearly.columns[df_pitching_yearly.columns.str.contains('value')])
df_pitching_yearly.columns = df_pitching_yearly.columns.str.replace('_label', '')

#make intitial page layout
layout = html.Div([
    html.Header([
        html.Div([
        html.H1('Player Comparison', id='title'),
        ], className='header'),
        html.Div([
            html.Div([
                html.A('Choose type:', id='dropdown-type-text'),
                dcc.Dropdown(
                    id='dropdown-batting-pitching',
                    options=[
                        {'label': 'Batting', 'value': 'batting'},
                        {'label': 'Pitching', 'value': 'pitching'}
                    ],
                    value = 'batting',
                    placeholder = 'Type:',
                    clearable = False)],
                    className='player-select-item'
                ),
            html.Div([
                html.A('Choose player 1:', id='dropdown-text-1'),
                dcc.Dropdown(
                    id='dropdown-player1',
                    placeholder = 'Select a player',
                    clearable = False)],
            className='player-select-item'),
            html.Div([
                html.A('Choose player 2:'),
                dcc.Dropdown(
                    id='dropdown-player2',
                    placeholder = 'Select a player',
                    clearable = False)],
            className='player-select-item'),
            html.Div([
                dbc.Button('Compare', id='compare-button', color="primary", className='compare-button-css', n_clicks=0)
            ], className='player-select-item')
        ], id='player-selection'),
        html.Div([
            dcc.Tabs(id='page-tabs', value='tab-1', children=[
                dcc.Tab(label='Overview', value='tab-1'),
                dcc.Tab(label='Stats', value='tab-2'),
            ]),
            html.Div(id='comparison-page-content')
        ])
    ], id='background')
], id='main')

#function used for making comparison graph
def make_comparison_bars(player1, player2, selected_stats, dfplayer1, dfplayer2):
    divlist = []
    for stat in selected_stats:
        stat_p1 = dfplayer1[stat].values
        stat_p2 = dfplayer2[stat].values

        if stat_p1 > stat_p2:
            color_p1 = '#00722e'
            color_p2 = '#c90202'
        elif stat_p1 == stat_p2:
            color_p1 = '#ed6300'
            color_p2 = '#ed6300'
        else:
            color_p1 = '#c90202'
            color_p2 = '#00722e'

        fig_player1 = go.Figure([go.Bar(
                    x=stat_p1,
                    orientation='h',
                    marker_color=color_p1,
                    showlegend=False,
                    width=0.3,
                    )])

        fig_player2 = go.Figure([go.Bar(
                    x=stat_p2,
                    orientation='h',
                    marker_color=color_p2,
                    showlegend=False,
                    width=0.3,
                    )])

        fig_player1.update_xaxes(visible = False, range=[(stat_p1[0] + stat_p2[0]), 0], showgrid=False)
        fig_player2.update_xaxes(visible = False, range=[0, (stat_p1[0] + stat_p2[0])], showgrid=False)
        fig_player1.update_yaxes(visible = False, showgrid=False)
        fig_player2.update_yaxes(visible = False, showgrid=False)

        fig_player1.update_layout(barmode='stack', plot_bgcolor = '#f0eded',
            height = 60, width=600, margin=dict(l=0, r=0, t=0, b=0))

        fig_player2.update_layout(barmode='stack', plot_bgcolor = '#f0eded',
            height = 60, width=600, margin=dict(l=0, r=0, t=0, b=0))

        div = html.Div([
            html.A(round(stat_p1[0],3), className='stat-item'),
            dcc.Graph(figure=fig_player1, config = {'staticPlot': True}, className='stat-graph-left'), 
            html.A(stat.upper(), className='stat-item-mid'),
            dcc.Graph(figure=fig_player2, config = {'staticPlot': True}, className='stat-graph-right'),
            html.A(round(stat_p2[0],3), className='stat-item')
            ], id='stat-'+stat, className='statdiv')

        divlist.append(div)
    return divlist

#layout of first tab 
tab1 = (
        html.Div([
            html.H2(className='player-name-title', id='player-title-1-tab1'),
            html.H2(className='player-name-title', id='player-title-2-tab1'),
        ], id='player-names'),
        html.Div([
            html.Div([
                html.A('Choose a statistic'),
                dcc.Dropdown(
                    className = 'stat-dropdown',
                    id = 'player1-stat-dropdown',
                    clearable = False
                ),
            ], className = 'stat-dropdown-p1'),
            html.Div([
                html.A('Choose a statistic'),
                dcc.Dropdown(
                    className = 'stat-dropdown',
                    id = 'player2-stat-dropdown',
                    clearable = False
                    )
            ], className = 'stat-dropdown-p2')
        ], id='container-stat-dropdowns', className = 'container-stat-dropdown-css', style={'display':'none'}
        ),
        html.Div([
            html.Div(id='player1-years', className='bargraph-p1'),
            html.Div(id='player2-years', className='bargraph-p2'),
        ], className='bar-graphs'),
        html.Div(id='player-graph'))

#layout of second tab
tab2 = (html.Div([
                    html.H2(className='player-name-title', id='player-title-1-tab2'),
                    html.H2(className='player-name-title', id='player-title-2-tab2'),
                ], id='player-names'),
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Dropdown(
                                className='dd-career1',
                                id='dropdown-career-yearly-p1',
                                options=[
                                    {'label': 'Career', 'value': 'career'},
                                    {'label': 'Yearly', 'value': 'yearly'}
                                ],
                                value = 'career',
                                clearable = False),
                        ], id='career-dd-p1', className='dropdown-careers'),
                        html.Div([
                            dcc.Dropdown(
                                className='dropdown-years1',
                                id='select-year-player1',
                                clearable=False
                            ),
                            dcc.Dropdown(
                                className='dropdown-leagues1',
                                id='select-league-player1',
                                clearable = False
                            )
                        ], id='year-league-player1', className='select-year-league', style={'display':'none'}),
                    ], className='player1-dropdowns'),

                    html.Div([
                        html.Div([
                            dcc.Dropdown(
                                className='dd-career2',
                                id='dropdown-career-yearly-p2',
                                options=[
                                    {'label': 'Career', 'value': 'career'},
                                    {'label': 'Yearly', 'value': 'yearly'}
                                ],
                                value = 'career',
                                clearable = False)
                        ], id='career-dd-p2', className='dropdown-careers'),
                        html.Div([
                            dcc.Dropdown(
                                className='dropdown-years2',
                                id='select-year-player2',
                                clearable = False
                            ),
                            dcc.Dropdown(
                                className='dropdown-leagues2',
                                id='select-league-player2',
                                clearable = False
                            )
                            ], id='year-league-player2', className='select-year-league', style={'display':'none'}),
                        ], className='player2-dropdowns'),
                ], id= 'dropdown-years-leagues', className='dropdown-years-leagues-css'),
                html.Div([
                    dcc.Dropdown(placeholder = 'Select stats',
                        id = 'compare-stat-dd',
                        multi = True,
                        className = 'stats-selector',
                        persistence=True,
                        persistence_type='local'
                    ),
                ]),
                html.Div(id='comparison-div', className = 'comparison-div-css'))

#change player dropdown options based on batting/pitching selection
@app.callback(
    Output('dropdown-player1', 'options'),
    Output('dropdown-player2', 'options'),
    Input('dropdown-batting-pitching', 'value'))
def players_in_dropdown(batting_pitching):
    if batting_pitching == 'batting': 
        dropdown_values = [{'label': i, 'value': i} for i in df_batting_career.PlayerName.unique()]
    elif batting_pitching == 'pitching':
        dropdown_values = [{'label': i, 'value': i} for i in df_pitching_career.PlayerName.unique()]
    else:
        dropdown_values = []
    return dropdown_values, dropdown_values

#callback for changing tabs
@app.callback(
    Output('comparison-page-content', 'children'),
    Input('page-tabs', 'value'),
    Input('compare-button', 'n_clicks'),
    State('dropdown-player2', 'value'))
def test_button(selectedtab, compare_button, p2_dd):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if selectedtab == 'tab-1' and p2_dd != None and ('compare-button' in changed_id or compare_button > 0):
        return tab1
    if selectedtab == 'tab-2' and p2_dd != None and ('compare-button' in changed_id or compare_button > 0):
        return tab2
    else:
        return html.Div('Please select two players', id='choose-player')

###Tab 1
#Show selected players in titles
@app.callback(
    Output('player-title-1-tab1', 'children'),
    Output('player-title-2-tab1', 'children'),
    Input('compare-button', 'n_clicks'),    
    State('dropdown-player1', 'value'),
    State('dropdown-player2', 'value'))
def comparison_bars_part1(compare_button, player1, player2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'compare-button' in changed_id or compare_button > 0:
        return player1, player2
    else:
        return [], []

#Shows stat dropdowns when compare button is clicked and fills stat dropdowns with options
@app.callback(
    Output('container-stat-dropdowns', 'style'),
    Output('player1-stat-dropdown', 'options'),
    Output('player2-stat-dropdown', 'options'),
    Output('player1-stat-dropdown', 'value'),
    Output('player2-stat-dropdown', 'value'),  
    Input('compare-button', 'n_clicks'),
    State('dropdown-batting-pitching', 'value'),
    State('dropdown-player1', 'value'),
    State('dropdown-player2', 'value'))
def show_stat_dropdown(compare_button, bat_or_pitch, p1_dd, p2_dd):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'compare-button' in changed_id or compare_button > 0:
        if p1_dd != None and p2_dd != None:
            if bat_or_pitch == 'batting':
                bat_stat_list = df_batting_career.select_dtypes(exclude='object').columns
                #bat_stat_list = bat_stat_list.drop('Year')
                stat_options_batting = [{'label': i, 'value': i} for i in bat_stat_list]
                return {'display':'flex'}, stat_options_batting, stat_options_batting, 'g', 'g'
            if bat_or_pitch == 'pitching':
                pit_stat_list = df_pitching_career.select_dtypes(exclude='object').columns
                stat_options_pitching = [{'label': i, 'value': i} for i in pit_stat_list]
                return {'display':'flex'}, stat_options_pitching, stat_options_pitching, 'gs', 'gs'
        else:
            return {'display':'none'}, [], [], [], []
    else:
        return {'display':'none'}, [], [], [], []

#Callback to make bar graphs based on chosen players and chosen statistic
@app.callback(
    Output('player1-years', 'children'),
    Output('player2-years', 'children'),
    Input('compare-button', 'n_clicks'),
    Input('player1-stat-dropdown', 'value'),
    Input('player2-stat-dropdown', 'value'),
    State('dropdown-batting-pitching', 'value'),
    State('dropdown-player1', 'value'),
    State('dropdown-player2', 'value'))
def update_bar_graph1(compare_button, stat_p1, stat_p2, bat_pitch, dropdown_player1, dropdown_player2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'compare-button' in changed_id or compare_button > 0:  
        if dropdown_player1 != None and dropdown_player2 != None:
            if bat_pitch == 'batting':
                fig_bar1 = px.bar(df_batting_yearly[df_batting_yearly['PlayerName'] == dropdown_player1].round(3),
                    x = 'Year', y = stat_p1, color='League', barmode='group', text=stat_p1)
                
                fig_bar1.update_xaxes(dtick=1)
                fig_bar1.update_layout(paper_bgcolor = '#f0eded')
                fig_bar1.update_traces(textposition="outside")

                bar1 = dcc.Graph(id='player1-bar-graph', className='bar-graph-p1', figure = fig_bar1)

                fig_bar2 = px.bar(df_batting_yearly[df_batting_yearly['PlayerName'] == dropdown_player2].round(3),
                    x = 'Year', y = stat_p2, color='League', barmode='group', text=stat_p2)
                
                fig_bar2.update_xaxes(dtick=1)
                fig_bar2.update_layout(paper_bgcolor = '#f0eded')
                fig_bar2.update_traces(textposition="outside")

                bar2 = dcc.Graph(id='player2-bar-graph', className='bar-graph-p2', figure = fig_bar2)
            
            if bat_pitch == 'pitching':
                fig_bar1 = px.bar(df_pitching_yearly[df_pitching_yearly['PlayerName'] == dropdown_player1].round(3),
                    x = 'Year', y = stat_p1, color='League', barmode='group', text=stat_p1)
                
                fig_bar1.update_xaxes(dtick=1)
                fig_bar1.update_layout(paper_bgcolor = '#f0eded')
                fig_bar1.update_traces(textposition="outside")

                bar1 = dcc.Graph(id='player1-bar-graph', className='bar-graph-p1', figure = fig_bar1)

                fig_bar2 = px.bar(df_pitching_yearly[df_pitching_yearly['PlayerName'] == dropdown_player2].round(3),
                    x = 'Year', y = stat_p2, color='League', barmode='group', text=stat_p2)
                
                fig_bar2.update_xaxes(dtick=1)
                fig_bar2.update_layout(paper_bgcolor = '#f0eded')
                fig_bar2.update_traces(textposition="outside")

                bar2 = dcc.Graph(id='player2-bar-graph', className='bar-graph-p2', figure = fig_bar2)
            return bar1, bar2
        else:
            return [], []
    else:
        return [], []

#Callback to make horizontal bargraphs for 4 most important stats
@app.callback(
    Output('player-graph', 'children'),
    Input('compare-button', 'n_clicks'),
    State('dropdown-batting-pitching', 'value'),
    State('dropdown-player1', 'value'),
    State('dropdown-player2', 'value'))
def update_graph(compare_button, drop_pitch, dropdown_player1, dropdown_player2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'compare-button' in changed_id or compare_button > 0:   
        if dropdown_player1 != None and dropdown_player2 != None:
            if drop_pitch == 'batting':
                new_df = df_batting_career.loc[
                    (df_batting_career['PlayerName'] == dropdown_player1) 
                    | (df_batting_career['PlayerName'] == dropdown_player2)]

                fig = make_subplots(rows=1, cols=4, subplot_titles=('SLG', 'OPS', 'PA', 'H'), 
                    shared_yaxes=True)

                fig.add_trace(go.Bar(x=new_df['slg'],
                        y=new_df['PlayerName'], orientation='h', marker_color='indianred'),
                        row=1, col=1)

                fig.add_trace(go.Bar(x=new_df['ops'],
                        y=new_df['PlayerName'], orientation='h', marker_color='indianred'),
                        row=1, col=2)

                fig.add_trace(go.Bar(x=new_df['pa'],
                        y=new_df['PlayerName'], orientation='h', marker_color='indianred'),
                        row=1, col=3)

                fig.add_trace(go.Bar(x=new_df['h'],
                        y=new_df['PlayerName'], orientation='h', marker_color='indianred'),
                        row=1, col=4)

                fig.update_layout(showlegend=False, height = 100, paper_bgcolor = '#f0eded', margin=dict(l=0, r=0, t=20, b=0))
            
            if drop_pitch == 'pitching':
                new_df = df_pitching_career.loc[
                    (df_pitching_career['PlayerName'] == dropdown_player1) 
                    | (df_pitching_career['PlayerName'] == dropdown_player2)]

                fig = make_subplots(rows=1, cols=3, subplot_titles=('IP', 'SO', 'WHIP'), 
                    shared_yaxes=True)

                fig.add_trace(go.Bar(x=new_df['ip'],
                        y=new_df['PlayerName'], orientation='h', marker_color='indianred'),
                        row=1, col=1)

                fig.add_trace(go.Bar(x=new_df['so'],
                        y=new_df['PlayerName'], orientation='h', marker_color='indianred'),
                        row=1, col=2)

                fig.add_trace(go.Bar(x=new_df['whip'],
                        y=new_df['PlayerName'], orientation='h', marker_color='indianred'),
                        row=1, col=3)

                fig.update_layout(showlegend=False, height = 100, paper_bgcolor = '#f0eded', margin=dict(l=0, r=0, t=20, b=0))

            return (html.H3('Career statistics', className='title-hbars'),
                dcc.Graph(id='indicator-graphic', figure = fig))
        else:
            return html.Div('Please select two players', id='choose-player')
    else:
        return html.Div('Please select two players', id='choose-player')


###Tab 2
#Show selected players in titles
@app.callback(
    Output('player-title-1-tab2', 'children'),
    Output('player-title-2-tab2', 'children'),
    Input('compare-button', 'n_clicks'),    
    State('dropdown-player1', 'value'),
    State('dropdown-player2', 'value'))
def comparison_bars_part2(compare_button, player1, player2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'compare-button' in changed_id or compare_button > 0:
        return player1, player2
    else:
        return [], []

#Fills stat dropdown
@app.callback(
    Output('compare-stat-dd', 'options'),
    #Output('compare-stat-dd', 'value'),
    Input('compare-button', 'n_clicks'),
    State('dropdown-batting-pitching', 'value'))
def fill_stat_dropdown(compare_button, bat_pitch):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'compare-button' in changed_id or compare_button > 0:
        if bat_pitch == 'batting':
            return  [{'label': i, 'value': i} for i in df_batting_career.select_dtypes(exclude='object').columns]
                #['slg', 'ops', 'pa', 'h']]
        if bat_pitch == 'pitching':
            return  [{'label': i, 'value': i} for i in df_pitching_career.select_dtypes(exclude='object').columns]
                #['ip', 'so', 'whip']]

#Shows year and career dropdowns when yearly is selected
@app.callback(
    Output('year-league-player1', 'style'),
    Output('year-league-player2', 'style'),
    Input('dropdown-career-yearly-p1', 'value'),
    Input('dropdown-career-yearly-p2', 'value'))
def show_year_dropdown(dropdown_career_p1, dropdown_career_p2):
    if dropdown_career_p1 == 'career': 
        dd_year_p1 = {'display':'none'}
    elif dropdown_career_p1 == 'yearly':
        dd_year_p1 = {'display':'flex'}

    if dropdown_career_p2 == 'career': 
        dd_year_p2 = {'display':'none'}
    elif dropdown_career_p2 == 'yearly':
        dd_year_p2 = {'display':'flex'}

    else: 
        dd_year_p1 = {'display':'none'}
        dd_year_p2 = {'display':'none'}
    return dd_year_p1, dd_year_p2

#Fills year dropdown with options based on batting/pitching dropdown selection
@app.callback(
    Output('select-year-player1', 'options'),
    Output('select-year-player2', 'options'),
    Output('select-year-player1', 'value'),
    Output('select-year-player2', 'value'),
    Input('compare-button', 'n_clicks'), 
    State('dropdown-batting-pitching', 'value'),
    State('dropdown-player1', 'value'),
    State('dropdown-player2', 'value'))
def years_in_dropdown(compare_button, bat_pitch, dd_p1, dd_p2):
    if dd_p1 != None and dd_p1 != None:
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if 'compare-button' in changed_id or compare_button > 0:
            if bat_pitch == 'batting':
                dd_years_p1 = [{'label': i, 'value': i} for i in df_batting_yearly[df_batting_yearly['PlayerName'] == dd_p1]['Year'].unique()]
                dd_years_p2 = [{'label': i, 'value': i} for i in df_batting_yearly[df_batting_yearly['PlayerName'] == dd_p2]['Year'].unique()]
                dd_years_p1_value = df_batting_yearly[df_batting_yearly['PlayerName'] == dd_p1]['Year'].unique()[0]
                dd_years_p2_value = df_batting_yearly[df_batting_yearly['PlayerName'] == dd_p2]['Year'].unique()[0]
            elif bat_pitch == 'pitching': 
                dd_years_p1 = [{'label': i, 'value': i} for i in df_pitching_yearly[df_pitching_yearly['PlayerName'] == dd_p1]['Year'].unique()]
                dd_years_p2 = [{'label': i, 'value': i} for i in df_pitching_yearly[df_pitching_yearly['PlayerName'] == dd_p2]['Year'].unique()]
                dd_years_p1_value = df_pitching_yearly[df_pitching_yearly['PlayerName'] == dd_p1]['Year'].unique()[0]
                dd_years_p2_value = df_pitching_yearly[df_pitching_yearly['PlayerName'] == dd_p2]['Year'].unique()[0]
            else:
                dd_years_p1 = []
                dd_years_p2 = []
            return dd_years_p1, dd_years_p2, dd_years_p1_value, dd_years_p2_value
    else:
        return [], [], [], []

#Fills league dropdown with options based on batting/pitching dropdown selection
@app.callback(
    Output('select-league-player1', 'options'),
    Output('select-league-player2', 'options'),
    Output('select-league-player1', 'value'),
    Output('select-league-player2', 'value'),
    Input('select-year-player1', 'value'),
    Input('select-year-player2', 'value'),
    State('dropdown-batting-pitching', 'value'),
    State('dropdown-player1', 'value'),
    State('dropdown-player2', 'value'))
def fill_year_dd(year_dd1, year_dd2, dd_bat_pitch, player1_dd, player2_dd):
    if dd_bat_pitch == 'batting':
        league_options_p1 = [{'label': i, 'value': i} for i in df_batting_yearly[(
            df_batting_yearly['PlayerName'] == player1_dd) & (
            df_batting_yearly['Year'] == year_dd1)]['League'].unique()]
        league_options_p2 = [{'label': i, 'value': i} for i in df_batting_yearly[(
            df_batting_yearly['PlayerName'] == player2_dd) & (
            df_batting_yearly['Year'] == year_dd2)]['League'].unique()]
        league_value_p1 = df_batting_yearly[(
            df_batting_yearly['PlayerName'] == player1_dd) & (
            df_batting_yearly['Year'] == year_dd1)]['League'].unique()[0]
        league_value_p2 = df_batting_yearly[(
            df_batting_yearly['PlayerName'] == player2_dd) & (
            df_batting_yearly['Year'] == year_dd2)]['League'].unique()[0]

    elif dd_bat_pitch == 'pitching':
        league_options_p1 = [{'label': i, 'value': i} for i in df_pitching_yearly[(
            df_pitching_yearly['PlayerName'] == player1_dd) & (
            df_pitching_yearly['Year'] == year_dd1)]['League'].unique()]
        league_options_p2 = [{'label': i, 'value': i} for i in df_pitching_yearly[(
            df_pitching_yearly['PlayerName'] == player2_dd) & (
            df_pitching_yearly['Year'] == year_dd2)]['League'].unique()]
        league_value_p1 = df_pitching_yearly[(
            df_pitching_yearly['PlayerName'] == player1_dd) & (
            df_pitching_yearly['Year'] == year_dd1)]['League'].unique()[0]
        league_value_p2 = df_pitching_yearly[(
            df_pitching_yearly['PlayerName'] == player2_dd) & (
            df_pitching_yearly['Year'] == year_dd2)]['League'].unique()[0]

    else: 
        league_options_p1 = []
        league_options_p2 = []

    return league_options_p1, league_options_p2, league_value_p1, league_value_p2

#Callback to create comparison bars, used function defined at top
@app.callback(
    Output('comparison-div', 'children'),
    Input('dropdown-career-yearly-p1', 'value'),
    Input('dropdown-career-yearly-p2', 'value'),
    Input('select-year-player1', 'value'),
    Input('select-year-player2', 'value'),
    Input('select-league-player1', 'value'),
    Input('select-league-player2', 'value'),
    Input('compare-stat-dd', 'value'),
    State('dropdown-batting-pitching', 'value'),
    State('dropdown-player1', 'value'),
    State('dropdown-player2', 'value'))
def comparison_bars(car_yea_p1, car_yea_p2, year_p1, year_p2, league_p1, league_p2, selected_stats, bat_pit_type, player1, player2):
    if player1 != None and player2 != None:
        if selected_stats != None:
            if bat_pit_type == 'batting':
                if car_yea_p1 == 'career':
                    df_p1 = df_batting_career[df_batting_career['PlayerName'] == player1]
                elif car_yea_p1 == 'yearly':
                    df_p1 = df_batting_yearly[(
                        df_batting_yearly['PlayerName'] == player1) & (
                        df_batting_yearly['Year'] == year_p1) & (
                        df_batting_yearly['League'] == league_p1)]

                if car_yea_p2 == 'career':
                    df_p2 = df_batting_career[df_batting_career['PlayerName'] == player2]
                elif car_yea_p2 == 'yearly':
                    df_p2 = df_batting_yearly[(
                        df_batting_yearly['PlayerName'] == player2) & (
                        df_batting_yearly['Year'] == year_p2) & (
                        df_batting_yearly['League'] == league_p2)]
            
            elif bat_pit_type == 'pitching':
                if car_yea_p1 == 'career':
                    df_p1 = df_pitching_career[df_pitching_career['PlayerName'] == player1]
                elif car_yea_p1 == 'yearly':
                    df_p1 = df_pitching_yearly[(
                        df_pitching_yearly['PlayerName'] == player1) & (
                        df_pitching_yearly['Year'] == year_p1) & (
                        df_pitching_yearly['League'] == league_p1)]

                if car_yea_p2 == 'yearly':
                    df_p2 = df_pitching_yearly[(
                        df_pitching_yearly['PlayerName'] == player2) & (
                        df_pitching_yearly['Year'] == year_p2) & (
                        df_pitching_yearly['League'] == league_p2)]
                elif car_yea_p2 == 'career':
                    df_p2 = df_pitching_career[df_pitching_career['PlayerName'] == player2]
            
            div_list = make_comparison_bars(player1, player2, selected_stats, df_p1, df_p2)

            return (html.Div([
                        html.Div(div_list
                            , id='comparison-bar-graphs', className='comparison-bar-graphs-css')
                        ], id='numbers-content')
                    )
        else:
            return html.Div('Select stats!', id='choose-player')            
    else:
        return html.Div('Please select two players', id='choose-player')