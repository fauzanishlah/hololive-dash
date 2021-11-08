import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.QUARTZ],
    suppress_callback_exceptions=True,
    meta_tags = [{
        'name':'viewport',
        'content': 'width=device-width, initial-scale=1.0'
    }]
)

app.title = "Hololive Dashboard"

server = app.server