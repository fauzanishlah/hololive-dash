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
from numerize import numerize

# Read Data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
channel = pd.read_csv(DATA_PATH.joinpath("hololive.csv"))

total_views = numerize.numerize(int(channel['views'].sum()))
total_member = channel['full_name'].nunique()
total_sub = numerize.numerize(int(channel['subscribers'].sum()))
total_vid = numerize.numerize(int(channel['total_videos'].sum()))

view_content = [
    dbc.CardBody([
        html.H2(total_views, className="card-title"),
        html.P("Total Views", className="card-text")
    ])
]

member_content = [
    dbc.CardBody([
        html.H2(total_member, className="card-title"),
        html.P("Talents", className="card-text")
    ])
]

subs_content = [
    dbc.CardBody([
        html.H2(total_sub, className="card-title"),
        html.P("Total Subscribers", className="card-text")
    ])
]

video_content = [
    dbc.CardBody([
        html.H2(total_vid, className="card-title"),
        html.P("Videos", className="card-text")
    ])
]

fig = px.treemap(
    channel,
    path = [px.Constant("all"), 'branch', 'gen', 'full_name'],
    values=None,
#     values = 'subscribers'
)
fig.update_traces(
    root_color="lightgrey",
    # tiling = dict(
    #     orientation = 'v'
    # )
)
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(
        b=0,l=0,r=0
    ),
)


layout = dbc.Container([
    dbc.Row([
        dcc.Graph(
            id='main-graph',
            figure=fig
        )
    ], style={'margin-bottom':'0.7rem'}),
    dbc.Row([
        dbc.Col(dbc.Card(member_content)),

        dbc.Col(dbc.Card(subs_content)),

        dbc.Col(dbc.Card(video_content)),

        dbc.Col(dbc.Card(view_content)),
    ]),
])