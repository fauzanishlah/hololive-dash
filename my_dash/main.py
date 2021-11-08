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

total_views = channel['views'].sum()
total_member = channel['full_name'].nunique()
total_sub = channel['subscribers'].sum()
total_vid = channel['total_videos'].sum()

view_content = [
    dbc.CardBody([
        html.H2(f"{total_views:,}", className="card-title"),
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
        html.H2(f"{total_sub/1000000} M", className="card-title"),
        html.P("Total Subscribers", className="card-text")
    ])
]

video_content = [
    dbc.CardBody([
        html.H2(f"{total_vid:,}", className="card-title"),
        html.P("Videos", className="card-text")
    ])
]

fig = px.icicle(
    channel,
    path = [px.Constant("all"), 'branch', 'gen', 'full_name'],
#     values = 'subscribers'
    hover_data = ['subscribers']
)
fig.update_traces(
    root_color="lightgrey",
    tiling = dict(
        orientation = 'v'
    )
)
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)


layout = dbc.Container([
    dbc.Row([
        dcc.Graph(
            id='main-graph',
            figure=fig
        )
    ]),
    dbc.Row([
        dbc.Col(dbc.Card(member_content)),

        dbc.Col(dbc.Card(subs_content)),

        dbc.Col(dbc.Card(video_content)),

        dbc.Col(dbc.Card(view_content)),
    ]),
])