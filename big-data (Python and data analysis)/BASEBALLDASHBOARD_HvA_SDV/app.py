import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect pages to the app
from pages import home, league, compare, attribute_tabs, teamPage, data_table, helppage, add_player, mvp, tournaments
from server import app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    # Navigation bar layout
    html.Div([
        html.Nav([
            html.Li([
                dcc.Link('Home', href='/pages/home')
            ], className='current-page'),
            html.Li([
                dcc.Link('MVP', href='/pages/mvp')
            ], className='current-page'),
            html.Li([
                dcc.Link('Player', href='/pages/league')
            ], className='current-page'),
              html.Li([
                dcc.Link('Add player', href='/pages/add_player')
            ], className='current-page'),
            html.Li([
                dcc.Link('Compare', href='/pages/compare')
            ], className='current-page'),
            html.Li([
                dcc.Link('Top Stats', href='/pages/attribute_tabs')
            ], className='current-page'),
            html.Li([
                dcc.Link('Team', href='/pages/teamPage')
            ], className='current-page'),
            html.Li([
                dcc.Link('Data Table', href='/pages/data_table')
            ], className='current-page'),
            html.Li([
                dcc.Link('Help', href='/pages/helppage')
            ], className='current-page'),
            html.Li([
                dcc.Link('Tournaments', href='/pages/tournaments')
            ], className='current-page')
        ])
    ], id='list-nav'),

    html.Div(id='page-content', children=[])
])

# Check if page is selected else 'error'
@app.callback(
    Output(component_id='page-content', component_property='children'), 
    [Input(component_id='url', component_property='pathname')])
def display_page(pathname):
    if pathname == '/pages/home':
        return home.layout
    elif pathname == '/pages/mvp':
        return mvp.layout   
    elif pathname == '/pages/league':
        return league.layout
    elif pathname == '/pages/compare':
        return compare.layout
    elif pathname == '/pages/attribute_tabs':
        return attribute_tabs.layout
    elif pathname == '/pages/teamPage':
        return teamPage.layout
    elif pathname == '/pages/data_table':
        return data_table.layout
    elif pathname == '/pages/helppage':
        return helppage.layout   
    elif pathname == '/pages/add_player':
        return add_player.layout     
    elif pathname == '/pages/tournaments':
        return tournaments.layout         
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, dev_tools_ui=None,
    dev_tools_props_check=None, dev_tools_serve_dev_bundles=None, dev_tools_hot_reload=None,
    dev_tools_hot_reload_interval=None, dev_tools_hot_reload_watch_interval=None,
    dev_tools_hot_reload_max_retry=None, dev_tools_silence_routes_logging=None, dev_tools_prune_errors=None)

# if __name__ == '__main__':
#     # For Development only, otherwise use gunicorn or uwsgi to launch, e.g.
#     # gunicorn -b 0.0.0.0:8050 index:app.server
#     app.run_server(
#         port=8050,
#         host='0.0.0.0'
#     )