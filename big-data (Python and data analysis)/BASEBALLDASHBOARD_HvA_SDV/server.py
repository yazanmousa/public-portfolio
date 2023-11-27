import dash
import dash_bootstrap_components as dbc

# Dash
external_stylesheets = ['assets\style.css', dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, title='SDV Baseball Dashboard',  external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server
app.scripts.config.serve_locally=True
app.config.suppress_callback_exceptions = True