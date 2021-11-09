# Dash library
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from pandas.io.formats import style

from app import app

# For graph
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff

from numerize.numerize import numerize
import datetime

# data manipulation
import pandas as pd
import pathlib

# Read Data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
channel = pd.read_csv(DATA_PATH.joinpath("hololive.csv"))
video = pd.read_csv(DATA_PATH.joinpath("hololive_videos.csv"))

# Convert datatypes
video['published_date'] = pd.to_datetime(video['published_date'])
video['duration'] = pd.to_timedelta(video.duration).dt.total_seconds()

talent = channel.merge(video, how='right', on='channel_id')

folder_img = "assets\\main\\talent\\"
format_img = ".jpg"

talent_duration = [
    dbc.Col([
        dbc.Card([
            dbc.CardHeader("Video Duration Histogram"),
            dbc.CardBody(
                dcc.Graph(id='talent-duration-likelihood')
            ),
            dbc.CardFooter(
                dcc.Slider(
                    id='bin-duration',
                    min=10,
                    max=80,
                    step=1,
                    value=40,
                    tooltip={"placement": "bottom", "always_visible": True},
                )
            )
        ]),
    ]),
    dbc.Col([
        dbc.Card([
            dbc.CardHeader("Video Views Histogram"),
            dbc.CardBody(
                dcc.Graph(id='talent-views-likelihood'),
            ),
            dbc.CardFooter([
                dcc.Slider(
                    id='bin-views',
                    min=10,
                    max=80,
                    step=1,
                    value=40,
                    tooltip={"placement": "bottom", "always_visible": True},
                )
            ])
        ])
    ])
]

talent_card_video = [
    dbc.CardHeader(
        html.H5("Most Watched Video", className='card-title')
        ),
    dbc.CardBody(id='talent-video-most-watch')
]

talent_card_stats = dbc.Row([
    dbc.Col(
        dbc.CardImg(
            id='talent-card-img',
            src='assets\main\hololive.jpg',
            className="img-fluid rounded-start",
        ),
        className="col-md-4",
    ),
    dbc.Col(
        dbc.CardBody(
            id='talent-card-stats'
            ),
        className="col-md-8",
    ),
], align='center')

talent_stats_graph = [
    dbc.Col(
        dbc.Card([
            dbc.CardHeader("Duration to Views"),
            dbc.CardBody(
                dcc.Graph(id='talent-dur-views', figure={})
            )
        ]), style={'margin-bottom':'0.7rem'}
    ),
    dbc.Col(
        dbc.Card([
            dbc.CardHeader("Duration to Likes"),
            dbc.CardBody(dcc.Graph(id='talent-dur-likes'))
        ]), style={'margin-bottom':'0.7rem'}
    ),
    dbc.Col(
        dbc.Card([
            dbc.CardHeader("Views to Likes"),
            dbc.CardBody(dcc.Graph(id='talent-views-likes'))
        ]), style={'margin-bottom':'0.7rem'}
    ),
]

talent_video_graph = dbc.Card([
    dbc.CardHeader("Views Over Time"),
    dbc.CardBody(
        dcc.Graph(id='talent-video')
    )
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
    ], style={'margin-top':'1rem'}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                id='talent-card',
                children = [],
                className="mb-3",
                style={"maxWidth": "540px"},
            ),
        ),
        dbc.Col(
            dbc.Card(
                id='talent-card-video',
                className="mb-3"
            )
        )
    ], align="center", style={"margin-top":"1rem"}),
    dbc.Row(id='talent-video-graph', style={'margin-bottom':'0.5rem'}),
    dbc.Row(id='talent-stats-graph', align='center'),    
    dbc.Row(id='talent-duration-graph', align='center')
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
    options = [{'label':talent, 'value':talent} for talent in sorted(dff.full_name.unique())]
    return options

@app.callback(
    Output('talent-card', 'children'),
    Output('talent-card-video', 'children'),
    Output('talent-duration-graph', 'children'),
    Output('talent-stats-graph', 'children'),
    Output('talent-video-graph', 'children'),
    Input('talent-select', 'value')
)
def talent_select_card(talent_value):
    if talent_value == None:
        return [], [], [], [], []
    else:
        return talent_card_stats, talent_card_video,talent_duration, talent_stats_graph, talent_video_graph


# Talent Stats
@app.callback(
    Output('talent-card-stats', 'children'),
    Output('talent-video-most-watch', 'children'),
    Output('talent-card-img', 'src'),
    Input('talent-select', 'value')
)
def talent_card_name(talent_value):
    name = str(talent_value)
    df = channel.loc[channel['full_name'] == name]
    dff = talent.loc[talent['full_name'] == name]
    total_subs = numerize(int(df.iloc[0]["subscribers"]))
    total_view = numerize(int(df.iloc[0]["views"]))
    total_vid = df.iloc[0]["total_videos"]
    style = {'margin-bottom':'0'}

    child_stats = [
        html.H2(name, className='card-title'),
        html.P(f'Total Subscribers: {total_subs}', className='card-text', style=style),
        html.P(f'Total Videos: {total_vid}', className='card-text', style=style),
        html.P(f'Total Views: {total_view}', className='card-text', style=style),
    ]
    img_src = folder_img + name + format_img

    most_watched = dff.loc[dff['views_y'] == dff['views_y'].max()].iloc[0]
    title = most_watched['title']
    views = numerize(int(most_watched['views_y']))
    likes = numerize(int(most_watched['likes']))
    duration = datetime.timedelta(seconds=int(most_watched['duration']))
    vid_id = most_watched['video_id']
    child_video = [
        html.H5(title, className='card-title'),
        html.P([
            f'{duration} | {views} views | {likes} likes |',
            dbc.Button(
                "view video", 
                target="_blank",
                href=f'https://www.youtube.com/watch?v={vid_id}',
                outline=True,
                color="secondary",
            )
        ], className='card-text')
    ]
    return child_stats, child_video, img_src

@app.callback(
    Output('talent-duration-likelihood', 'figure'),
    Output('talent-views-likelihood', 'figure'),
    [Input('talent-select', 'value'),
    Input('bin-duration', 'value'),
    Input('bin-views', 'value')]
)
def talent_duration_likelihood(talent_value, bin_dur, bin_views):
    df = talent.loc[talent['full_name']==talent_value]
    df['duration'] = pd.to_timedelta(df['duration'], unit='S').astype('timedelta64[m]')
    fig_dur = px.histogram(
        df,
        x = 'duration',
        color_discrete_sequence=['#ffffff'] ,
        nbins=bin_dur,
        labels={'duration':'Duration(m)',}
    )
    fig_dur.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            t=0,b=0,l=0,r=0
        ),
    )
    fig_view = px.histogram(
        df,
        x = 'views_y',
        color_discrete_sequence=['#ffffff'] ,
        nbins=bin_views,
        labels={'views_y':'Views'}
    )
    fig_view.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            t=0,b=0,l=0,r=0
        ),
    )
    return fig_dur, fig_view

@app.callback(
    Output('talent-dur-views', 'figure'),
    Output('talent-dur-likes', 'figure'),
    Output('talent-views-likes', 'figure'),
    Input('talent-select', 'value')
)
def stats_graphs(talent_value):
    df_stats = talent.loc[talent['full_name'] == talent_value]
    df_stats['duration'] = pd.to_timedelta(df_stats['duration'], unit='S').astype('timedelta64[m]')

    fig_dur_view = px.scatter(
        df_stats,
        x='duration',
        y='views_y',
        labels={
            'views_y':'Views',
            'duration':'Duration (m)'
        },
        color_discrete_sequence=['#ffffff'] ,
    )
    fig_dur_view.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            t=0,b=0,l=0,r=0
        ),
    )

    fig_dur_likes = px.scatter(
        df_stats,
        x='duration',
        y='likes',
        labels={
            'likes':'Likes',
            'duration':'Duration (m)'
        },
        color_discrete_sequence=['#ffffff'] ,
    )
    fig_dur_likes.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            t=0,b=0,l=0,r=0
        ),
    )

    fig_view_likes = px.scatter(
        df_stats,
        x='views_y',
        y='likes',
        labels={
            'views_y':'Views',
            'likes':'Likes'
        },
        color_discrete_sequence=['#ffffff'] ,
    )
    fig_view_likes.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            t=0,b=0,l=0,r=0
        ),
    )

    return fig_dur_view, fig_dur_likes, fig_view_likes

@app.callback(
    Output('talent-video', 'figure'),
    Input('talent-select', 'value')
)
def video_talent(talent_value):
    df_vid = talent.loc[talent['full_name']==talent_value]
    # df_vid['published_date'] = pd.to_datetime(df_vid['published_date'])

    fig = px.line(
        df_vid, 
        x = 'published_date',
        y = 'views_y',
        hover_data=['title'],
        labels = {
            'published_date' : 'Date',
            'views_y':'Views',
        },
        color_discrete_sequence=['#ffffff'] ,
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            t=0,b=0,l=0,r=0
        ),
    )
    return fig