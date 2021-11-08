# Dash library
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

# For graph
import plotly.graph_objects as go
import plotly.express as px

# Dash app and layout
from app import app, server
from my_dash.navbar import Navbar
from my_dash import main, branch, gen, talent

app.layout = dbc.Container([
    Navbar,
    dcc.Location(id='url', refresh=False),
    dbc.Row(
        id='content-layout',
        children=[]
    ),
])

@app.callback(
    Output('content-layout', 'children'),
    [Input('url', 'pathname')]
)
def content_page(pathname):
    if pathname == '/branch':
        return branch.layout
    if pathname == '/gen':
        return gen.layout
    if pathname == '/talent':
        return talent.layout
    if pathname == '/':
        return main.layout

if __name__ == '__main__':
    app.run_server(debug=True)