#pylint: disable = line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order

import plotly.graph_objects as go
import pandas as pd
import dash_table
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from MySQL_data import SQL_Engine, execute_command, load_SQL_table
from dash.exceptions import PreventUpdate

from server import app
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import urllib

df_pitching = pd.read_sql_table('db_Pitching_Yearly', SQL_Engine) 
df_pitching.rename(columns={'PlayerName': 'Name','ip_label': 'IP', 'era_label': 'ERA', 'wlp_label': 'WLP', 'whip_label': 'WHIP', 'h9_label': 'H9',
                            'bb9_label': 'BB9', 'so9_label': 'SO9', 'sobb_label': 'SOBB'}, inplace=True)
df_pitching.drop(['ip_value', 'era_value', 'wlp_value', 'whip_value', 'h9_value', 'bb9_value', 'so9_value', 'sobb_value'], axis=1, inplace=True)
df_pitching.columns = map(lambda x: str(x).upper(), df_pitching.columns)

df_batting = pd.read_sql_table('db_Batting_Yearly', SQL_Engine)
df_batting.rename(columns={'MainPos': 'Main Position','PlayerName': 'Name', 'avg_label': 'AVG', 'obp_label': 'OBP', 'slg_label': 'SLG', 'ops_label': 'OPS', 'iso_label': 'ISO'}, inplace=True)
df_batting.drop(['avg_value', 'obp_value', 'slg_value', 'ops_value', 'iso_value', 'Pos_1b', 'Pos_2b', 'Pos_3b', 'Pos_c', 'Pos_cf', 'Pos_dh',
                 'Pos_lf', 'Pos_p', 'Pos_ph', 'Pos_pr', 'Pos_rf', 'Pos_ss'], axis=1, inplace=True)
df_batting.columns = map(lambda x: str(x).upper(), df_batting.columns)

df_batting['NAME'] = df_batting['NAME'].astype('category')
df_pitching['NAME'] = df_pitching['NAME'].astype('category')



# define layout and setup tabs
layout = html.Div([
    html.Header([

        #Tab 1
        html.Div([
        html.H1('Team Selection', id='title'),
        ], className='header'),
        dcc.Tabs(value='Batting-tab', children=[
            dcc.Tab(label='Team', value='team-tab', children=[
                html.Div([
                    html.H3('Batting line-up')
                ], className='team-batting-title'),
                html.Div([
                    html.Span('These are the players that you have selected for the batting line-up: ')
                ], className='team-batting-text'),

                
                # display batting table from batting tab                
                html.Div(id='battingTitleReplace'),
                    html.Div([
                        dash_table.DataTable(id='teamBattingTable',
                            columns=[{"name": i, "id": i} for i in df_batting.columns],
                            style_cell={'minWidth': 30, 'whiteSpace': 'normal'},
                            style_table={'height': '500px', 'width': '1500px', 'margin-left': '-260px', 'margin-bottom': '10px'},
                            data=df_batting.to_dict("rows"),
                            editable=True,
                            # creates an export button, this will produce an Excel file
                            export_format ="xlsx",
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current= 0,
                            page_size= 200,
                            fixed_rows={'headers': True},
                            style_cell_conditional=[    # align text columns to left. By default they are aligned to right
                            {
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['NAME', 'LEAGUE', 'MAIN POSITION']
                            ],
                            style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }],
                            style_header={
                                'backgroundColor': 'rgb(230, 230, 230)',
                                'fontWeight': 'bold'
                            }
                            )], id='battingDiv', className='team-batting-table'),

                    html.Div([
                    html.H3('Pitching team')
                            ], className='team-pitching-title'),
                    html.Div([
                    html.Span('These are the players you have selected for the pitching team: ')
                            ], className='team-pitching-text'),

                    # display pitching selection from pitching tab
                    html.Div(id='pitchingTitleReplace'),
                    html.Div([
                        dash_table.DataTable(id='teamPitchingTable',
                            columns=[{"name": i, "id": i} for i in df_pitching.columns],
                            style_cell={'minWidth': 45, 'whiteSpace': 'normal'},
                            style_table={'height': '500px', 'width': '1500px', 'margin-left': '-260px', 'margin-bottom': '100px'},
                            data=df_pitching.to_dict("rows"),
                            editable=True,
                            export_format ="xlsx",
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current= 0,
                            page_size= 200,
                            style_header={
                                'backgroundColor': 'rgb(230, 230, 230)',
                                'fontWeight': 'bold'
                            },
                            fixed_rows={'headers': True},
                            style_cell_conditional=[    # align text columns to left. By default they are aligned to right
                            {
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['NAME', 'LEAGUE', 'MAIN POSITION']
                            ],
                            style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }],
                            

                            )], id='pitchingDiv', className='team-pitching-table'),                       
            ], className='team-page'),

                    


            #tab 2
            dcc.Tab(label='Batting Selection', value='Batting-tab', children=[   
                html.Div([
                    html.H3('Batting line-up selection')
                ], className='pitchingbatting-title'),
                html.Div([
                    html.Span('Select names in the dropdown menu to add them to your team. Your team will appear in the Team tab.')
                ], className='pitchbatting-text'),

                html.Div([dcc.Dropdown(id='battingNamesSelect', className='team-batting-dropdown', multi=True,
                                            options=[{'label': name, 'value': name}
                                                        for name in df_batting['NAME'].unique()], 
                                                        persistence=True,
                                                        persistence_type='local'
                                                        )]),
                
                html.Div([
                dbc.Button(
                    'Click here to learn more about filtering',
                    id='more-info-button', className='filter-info-button'
                ),
                # make information box about how to use the table filtering functions
                dbc.Collapse([
                    dbc.Card(
                        dbc.CardBody('''Use basic operators to filter the table, like:
                                '=2020' in the year column to only see data from season 2020 or
                                '>10' in the Home Runs (HR) column to only show player who have hit more than 50 home runs.
                                Usable operators are Equal: =, Bigger than: >, Smaller than: <.
                                It's also possible to filter ons strings for the columns: 'Name', 'League'. (String filtering is case sensitive)''')
                    )], id='filter-collapse', className='filter-info-text'),
                ], className='filter-info'),

                html.Div([
                    dash_table.DataTable(
                            id='table_batting',
                            columns=[
                                {"name": i, "id": i} for i in df_batting.columns
                            ],
                            style_table={'height': '1000px'},
                            style_cell={'minWidth': 30, 'whiteSpace': 'normal'},
                            data=df_batting.to_dict('records'),
                            virtualization=True,
                            editable=True,
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current= 0,
                            page_size= 200,
                            # Makes the header of the table bold
                            style_header={
                                'backgroundColor': 'rgb(230, 230, 230)',
                                'fontWeight': 'bold'
                            },
                            fixed_rows={'headers': True},
                            # align text columns to left. By default they are aligned to right, the cells with numbers will be allighed to the left
                            style_cell_conditional=[    
                            {
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['NAME', 'LEAGUE', 'MAIN POSITION']
                            ],
                            # style odd rows to have a grey-ish background color
                            style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }],
                            
                        )], className='team-batting-table2'),
           
            ], className='batting-selection'),

            #Tab 3
            dcc.Tab(label='Pitching Selection', children=[ 
                html.Div([
                    html.H3('Pitcher line-up selection')
                ], className='pitchingbatting-title'),
                html.Div([
                    html.Span('Select names in the dropdown menu to add them to your team. Your team will appear in the Team tab.')
                ], className='pitchbatting-text'),

                dcc.Dropdown(id='pitchingNamesSelect', className='team-pitching-dropdown', options=[
                    {'label': i, 'value': i} for i in df_pitching.NAME.unique()
                            ], multi=True, placeholder='Select names for team',
                            persistence=True,
                            persistence_type='local'
                ),
                html.Div([
                dbc.Button(
                    'Click here to learn more about filtering',
                    id='pitch-more-info-button', className='filter-info-button'
                ),
                # make information box about how to use the table filtering functions
                dbc.Collapse([
                    dbc.Card(
                        dbc.CardBody('''Use basic operators to filter the table, like:
                                    '=2020' in the year column to only see data from season 2020 or
                                    '>50' in the Innings Pitched (IP) column to only show player who have pitched more than 50 innings.
                                    Usable operators are Equal: =, Bigger than: >, Smaller than: <.
                                    It's also possible to filter ons strings for the columns: 'Name', 'League'.''')
                    )], id='pitch-filter-collapse', className='filter-info-text'),
                ], className='filter-info'),
                
                html.Div([
                    dash_table.DataTable(
                            id='data_pitching',
                            columns=[
                                {"name": i, "id": i, "deletable": False, "selectable": True} for i in df_pitching.columns
                            ],
                            data=df_pitching.to_dict('records'),
                            style_table={'height': '1000px'},
                            style_cell={'minWidth': 25, 'whiteSpace': 'normal'},
                            # virtualization means the table will be rendered live this takes some load of the browser and keeps it snappy so it doesnt have to render al data at once
                            virtualization=True,
                            editable=True,
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current= 0,
                            page_size= 200,
                            style_header={
                                'backgroundColor': 'rgb(230, 230, 230)',
                                'fontWeight': 'bold'
                            },
                            fixed_rows={'headers': True},
                            # align text columns to left. By default they are aligned to right, the cells with numbers will be allighed to the left
                            style_cell_conditional=[   
                            {
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['NAME', 'LEAGUE', 'MAIN POSITION']
                            ],
                            # style odd rows to have a grey-ish background color
                            style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }],

                 )], className='team-pitching-table2'),

            ]),
        ], className='team-selection-tabs'),

        
    ])    
])


# Generate table with selected names from batting table players
@app.callback(Output('teamBattingTable', 'data'),
            Output('battingDiv', 'style'),
            Output('battingTitleReplace', 'children'),
            Input('battingNamesSelect', 'value'))
def filter_table(categories):
    if categories == []:
        return [], {'display':'none'}, html.H5('Select players in the Batting Selection tab to fill the table....')
    elif categories != None:
        df = df_batting[df_batting['NAME'].isin(categories)]
        return df.to_dict('rows'), {'display':'initial'}, []
    

# Generate table with selected names from pitching table players
@app.callback(Output('teamPitchingTable', 'data'),
            Output('pitchingDiv', 'style'),
            Output('pitchingTitleReplace', 'children'),
            Input('pitchingNamesSelect', 'value'))
def filter_table1(categories):
    if categories == []:
        return [], {'display':'none'}, html.H5('Select players in the Pitching Selection tab to fill the table....')
    elif categories != None:
        df = df_pitching[df_pitching['NAME'].isin(categories)]
        return df.to_dict('rows'), {'display':'initial'}, []


# Highlight selected column batting tab
@app.callback(
    Output('table_batting', 'style_data_conditional'),
    [Input('table_batting', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]


# Highlight selected column pitching tab
@app.callback(
    Output('data_pitching', 'style_data_conditional'),
    [Input('data_pitching', 'selected_columns')]
)
def update_styles1(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]
