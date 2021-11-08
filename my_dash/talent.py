# Dash library
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app

# For graph
import plotly.graph_objects as go
import plotly.express as px

# data manipulation
import pandas as pd

import pathlib
# Read Data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
channel = pd.read_csv(DATA_PATH.joinpath("hololive.csv"))

folder_img = "assets\\main\\talent\\"
format_img = ".jpg"

talent_card_content = dbc.Row([
    dbc.Col(
        dbc.CardImg(
            id='talent-card-img',
            src='assets\main\hololive.jpg',
            className="img-fluid rounded-start",
        ),
        className="col-md-4",
    ),
    dbc.Col(
        dbc.CardBody([
            html.H2(id='talent-card-name')
        ]),
        className="col-md-8",
    ),
])

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Select(
                id='talent-branch-select',
                options = [
                    {"label":"Hololive Japan", "value":"JP"},
                    {"label":"Hololive Indonesia", "value":"ID"},
                    {"label":"Hololive English", "value":"EN"}
                ],
                placeholder="Select branch..."
            )
        ),
        dbc.Col(
            dbc.Select(
                id='talent-gen-select',
                options = [],
                placeholder="Select gen..."
            )
        ),
        dbc.Col(
            dbc.Select(
                id='talent-select',
                options = [],
                placeholder="Select talent..."
            )
        ),
    ]),
    dbc.Row([
        dbc.Card(
            id='talent-card',
            children = [],
            className="mb-3",
            style={"maxWidth": "540px"},
        )
    ])
])

@app.callback(
    Output('talent-gen-select', 'options'),
    Input('talent-branch-select', 'value')
)
def talent_gen_select(branch_value):
    df = channel.copy()
    dff = df.loc[df['branch'] == branch_value]
    options = [{'label':gen, 'value':gen} for gen in sorted(dff.gen.unique())]
    return options

@app.callback(
    Output('talent-select', 'options'),
    Input('talent-gen-select', 'value')
)
def talent_gen_select(gen_value):
    df = channel.copy()
    dff = df.loc[df['gen'] == gen_value]
    options = [{'label':'Talent', 'value':3, 'disabled':True}]
    options2 = [{'label':talent, 'value':talent} for talent in sorted(dff.full_name.unique())]
    options.extend(options2)
    return options

@app.callback(
    Output('talent-card', 'children'),
    Input('talent-select', 'value')
)
def talent_select_card(talent):
    if talent == None:
        return []
    else:
        return talent_card_content

@app.callback(
    Output('talent-card-name', 'children'),
    Output('talent-card-img', 'src'),
    Input('talent-select', 'value')
)
def talent_card_name(talent):
    img_src = folder_img + str(talent) + format_img
    return str(talent), img_src