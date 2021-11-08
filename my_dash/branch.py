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

layout= dbc.Container([
    dbc.Row(
        dbc.Select(
            id='branch-select',
            options=[
                {"label":"Hololive Japan", "value":"JP"},
                {"label":"Hololive Indonesia", "value":"ID"},
                {"label":"Hololive English", "value":"EN"}
            ],
            value="ID"
        )
    ),

    dbc.Row([
        dbc.Col(
            id='branch-card-member',
            children=[]
        ),
        dbc.Col(
            id='branch-table-member',
            children=[]
        )
    ])
])

@app.callback(
    [Output('branch-table-member', 'children'),
    Output('branch-card-member', 'children')],
    [Input('branch-select', 'value')]
)
def branch_member(branch_value):
    df = channel.copy()
    # Creating Table
    df_table = df.loc[df['branch'] == branch_value, ['full_name','channel_name', 'subscribers']]
    table = dbc.Table.from_dataframe(df_table)
    card = []
    return table, card
