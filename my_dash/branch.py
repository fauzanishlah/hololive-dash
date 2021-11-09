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
from numerize.numerize import numerize

# Read Data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
channel = pd.read_csv(DATA_PATH.joinpath("hololive.csv"))

branch_stats = [
    dbc.Col(id='branch-gen-subs'),
    dbc.Col(id='branch-gen-views'),
    dbc.Col(id='branch-gen-videos'),
]
layout= dbc.Container([
    dbc.Row(
        dbc.Select(
            id='branch-select',
            options=[
                {"label":"Hololive Japan", "value":"JP"},
                {"label":"Hololive Indonesia", "value":"ID"},
                {"label":"Hololive English", "value":"EN"}
            ],
            placeholder="Select branch ..."
        ), style={'margin-top':'0.8rem'}
    ),

    dbc.Row(id='branch-stats', style={'margin-top':'0.8rem'})
])

@app.callback(
    Output('branch-stats', 'children'),
    Input('branch-select', 'value')
)
def show_branch_stats(branch_value):
    if branch_value == None:
        return []
    else:
        return branch_stats

@app.callback(
    Output('branch-gen-subs', 'children'),
    Input('branch-select', 'value')
)
def branch_subs(branch_value):
    df = channel.loc[channel['branch']==branch_value]
    fig = go.Figure(
        data = [
            go.Pie(labels=df['gen'], values=df['subscribers'], hole=.5)
        ]
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            t=0,b=0,l=0,r=0
        ),
        showlegend=False
    )
    total_subs = numerize(int(df['subscribers'].sum()))
    branch_gen_subs = dbc.Card([
        dbc.CardHeader("Subscribers"), 
        dbc.CardBody(
            dcc.Graph(
                figure=fig
            )
        ),
        dbc.CardFooter(f"total: {total_subs}")
    ]) 
    return branch_gen_subs

@app.callback(
    Output('branch-gen-views', 'children'),
    Input('branch-select', 'value')
)
def branch_views(branch_value):
    df = channel.loc[channel['branch']==branch_value]
    fig = go.Figure(
        data = [
            go.Pie(labels=df['gen'], values=df['views'], hole=.5)
        ]
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            t=0,b=0,l=0,r=0
        ),
        showlegend=False
    )
    total_views = numerize(int(df['views'].sum()))
    branch_gen_views = dbc.Card([
        dbc.CardHeader("Views"), 
        dbc.CardBody(
            dcc.Graph(
                figure=fig
            )
        ),
        dbc.CardFooter(f"total: {total_views}")
    ]) 
    return branch_gen_views

@app.callback(
    Output('branch-gen-videos', 'children'),
    Input('branch-select', 'value')
)
def branch_videos(branch_value):
    df = channel.loc[channel['branch']==branch_value]
    fig = go.Figure(
        data = [
            go.Pie(labels=df['gen'], values=df['total_videos'], hole=.5)
        ]
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            t=0,b=0,l=0,r=0
        ),
        showlegend=False
    )
    total_vid = numerize(int(df['total_videos'].sum()))
    branch_gen_videos = dbc.Card([
        dbc.CardHeader("# Videos"), 
        dbc.CardBody(
            dcc.Graph(
                figure=fig
            )
        ),
        dbc.CardFooter(f"total: {total_vid}")
    ]) 
    return branch_gen_videos
# @app.callback(
#     Output('branch-card-member', 'children'),
#     Input('branch-select', 'value')
# )
# def branch_member(branch_value):
#     # df = channel.copy()

#     # # # Creating Table
#     # # df_table = df.loc[df['branch'] == branch_value, ['full_name','channel_name', 'subscribers']]
#     # # table = dbc.Table.from_dataframe(df_table)

#     return branch_card_container
