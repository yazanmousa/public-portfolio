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


# Import datasets
df_career = pd.read_sql_table('db_Pitching_Career', SQL_Engine)
df_yearly = pd.read_sql_table('db_Pitching_Yearly', SQL_Engine)

# Round numeric values to 3 decimals
df_career = df_career.round(3)
df_yearly = df_yearly.round(3)

# Rename column names
df_career = df_career.rename(columns={'ip_label':'ip', 'era_label':'era', 'wlp_label':'wlp', 'whip_label':'whip', 'h9_label':'h9', 'bb9_label':'bb9', 'so9_label':'so9', 'sobb_label':'sobb'})
df_yearly = df_yearly.rename(columns={'ip_label':'ip', 'era_label':'era', 'wlp_label':'wlp', 'whip_label':'whip', 'h9_label':'h9', 'bb9_label':'bb9', 'so9_label':'so9', 'sobb_label':'sobb'})
column_name = ['gs','g', 'ip', 'h', 'r', 'er', 'bb', 'so', 'hbp', 'ibb', 'ab', 'bf', 'fo', 'go', 'np', 'Win', 'Loss', 'Save', 'era', 'wlp', 'whip', 'h9', 'bb9', 'so9', 'sobb']

# Layout dash page
layout = html.Div([
    # Selectors/dropdowns
    html.Div([
        # Input for selecting the number of players
        html.Div([
            html.Label('Select number of players: ', className='label-attribute'),
            dcc.Input(
                id='input-player-count',
                className= 'dropdown-attribute2',
                type='number',
                placeholder=''
            )
        ]),
        # Career or Yearly stats
        html.Div([
            html.Label('Select type: ', className='label-attribute'),
            dcc.Dropdown(
                id='pitching-dropdown-career-yearly',
                options=[
                    {'label': 'Career', 'value': 'career'},
                    {'label': 'Yearly', 'value': 'yearly'}                    
                ],
                placeholder='Stat-type',
                className='dropdown-attribute'
            )
        ]),
        # Yearly - year pitching-dropdown
        html.Div([
            dcc.Dropdown(
                id='pitching-dropdown-years',
                className='dropdown-attribute-year',
                placeholder='Select year'            )
        ]),           
        # Stat sorting
        html.Div([
            html.Label('Order by stat:', className='label-attribute'),
            dcc.Dropdown(
                id='pitching-dropdown-stats',
                className= 'dropdown-attribute',
                options=[{'label': i, 'value': i} for i in column_name
                ],
                placeholder='Sort by'
            )
        ], className='dropdown-stats-css')
    ]),
    # Table
    html.Div([
        dt.DataTable(
            id='pitching-player-table',
            style_cell={'textAlign': 'center'},
            style_header={'fontWeight': 'bold'},
            columns=[
                {'name': 'Playername', 'id': 'PlayerName'}] +
                [{'name': i, 'id':i} for i in column_name]
            ,
            style_table={
                'overflowY':'scroll',
                'height' : '700px'
            },
            filter_action='native'
        )
    ], className='player-table-css')
])

# Yearly - year pitching-dropdown show
@app.callback(
    Output('pitching-dropdown-years', 'style'),
    [Input('pitching-dropdown-career-yearly', 'value')]
)
def show_year_dropdown(career_or_yearly):
    show_year = {'display':'none'}
    if career_or_yearly != None:
        if career_or_yearly == 'yearly':
            show_year = {'display':''}
    return show_year

# Yearly - year pitching-dropdown fill
@app.callback(
    Output('pitching-dropdown-years', 'options'),
    [Input('pitching-dropdown-career-yearly', 'value')]
)
def update_year_dropdown(career_or_yearly):
    year_options = []
    years = []
    if career_or_yearly != None:
        if career_or_yearly == 'yearly':
            for i in df_yearly.Year.unique():
                years.append(i)
                years.sort(reverse=True)
            year_options = [{'label':i, 'value':i} for i in years]
    return year_options

# Selector callback making table
@app.callback(
    [Output('pitching-player-table', 'data'),
    Output('pitching-player-table', 'columns')],
    [Input('input-player-count', 'value'),
    Input('pitching-dropdown-stats', 'value'),
    Input('pitching-dropdown-career-yearly', 'value'),
    Input('pitching-dropdown-years', 'value')],
    [State('pitching-player-table', 'columns')]
    )
def update_table(input_number, sort_stat, career_yearly, years, column):
    table = None
    if sort_stat != None and career_yearly != None:
        if career_yearly == 'career':
            table = df_career
            table = table.sort_values(by=[sort_stat], ascending=False)
            table = table.head(input_number).to_dict('records')
        elif career_yearly == 'yearly':
            table = df_yearly
            if {'name': 'League', 'id': 'League'} not in column:
                column.insert(1, {'name': 'League', 'id': 'League'})
            if {'name': 'Year', 'id': 'Year'} not in column:
                column.insert(2, {'name': 'Year', 'id': 'Year'})
            table = table.sort_values(by=[sort_stat], ascending=False)
            if years is None:
                table = table.head(input_number).to_dict('records')
            elif years != None:
                table = table[table['Year'] == years]
                table = table.head(input_number).to_dict('records')
    return table, column

# Update color of max values
@app.callback(
    Output('pitching-player-table', 'style_data_conditional'),
    [Input('pitching-player-table', 'data')],
    [State('pitching-dropdown-stats', 'value'),
    State('pitching-dropdown-career-yearly', 'value')]
    )
def update_style(data, sort_stat, career_yearly):
    conditional_style = []
    if data != None:
        for item in column_name:
            max_value = max(data, key=lambda x : x.get(item))
            style = {
                'if':{
                    'column_id' : item, 
                    'filter_query': '{{{}}} = {}'.format(item, max_value.get(item))
                },
                'backgroundColor':'lightblue'
            }
            conditional_style.append(style)
    return conditional_style