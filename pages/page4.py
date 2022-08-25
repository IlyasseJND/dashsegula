# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 12:40:34 2022

@author: JOUNAIDI
"""
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.tools import mpl_to_plotly
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np
import pandas as pd
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

def month_to_season(month):
    a= month%12 // 3 + 1
    if a==1:
        return 'winter'
    elif a==2:
        return 'spring'
    elif a==3:
        return 'summer'
    else:
        return 'fall'

def time_variables(df):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['year'] = df.index.year
    df['month'] = df.index.month
    df['hour'] = df.index.hour
    df['weekday'] = df.index.strftime('%A')
    df['season'] = df['month'].apply(month_to_season)


layout = html.Div([
    dbc.Navbar(children=[
        dbc.NavItem(dbc.NavLink(children=dbc.Button("base de données",color="success"), href="/")),
        dbc.NavItem(dbc.NavLink(children=dbc.Button("informations statistiques",color="success"), href="/page1")),
        dbc.NavItem(dbc.NavLink(dbc.Button("Graphes statistique",color="success"), href="/page4")),
        dbc.NavItem(dbc.NavLink(dbc.Button("courbes",color="success"), href="/page2")),
        dbc.NavItem(dbc.NavLink(dbc.Button("comparaisons de consommations",color="success"), href="/page3")),
        dbc.NavItem(dbc.NavLink(dbc.Button("Heatmaps",color="success"), href="/page5")),
        dbc.NavItem(dbc.NavLink(dbc.Button("Correlation",color="success"), href="/page6")),],
         color="primary",),
    html.H4('Graphes statistique'),

    html.H5('Choix des axes :'),
    html.P('axe des x :'),
    dcc.RadioItems(
        id='x-axis', 
        options=['hour', 'weekday', 'month','season'],
        value='hour', 
        inline=True
    ),
    html.P(' '),
    html.P('axe des y :'),
    dcc.RadioItems(
        id='y-axis', 
        # options=['Socket', 'Light'],
        # value=False, 
        inline=True
    ),
    html.P(' '),
    html.H5('Boites à moustache :'),

    dcc.Graph(id="graph_boxx"),
    html.H5('Courbe de la moyenne sur axe des x :'),

    dcc.Graph(id="graph_mean"),

    # html.H5('Courbe de la moyenne par jour et par saison :'),

    # dcc.Graph(id="graph_mean_ds"),

    
])



@dash_app.callback(
    Output('y-axis', 'options'),Output('y-axis', 'value'),
    Input('stored-conscol', 'data'))
def display_value(col):
    col=pd.DataFrame(col)["0"].values.tolist()
    return col,col[0]

# @dash_app.callback(
#     Output('graph_boxx', 'figure'),
#     Input('y-axis', 'value'),
#     Input('x-axis', 'value'),
#     Input('stored-conscol', 'data'),
#     Input('stored-data', 'data'))
# def update_figure(yv,xv,col,data):
#     col=pd.DataFrame(col)["0"].values.tolist()
#     print(yv)
#     df=pd.DataFrame(data)
#     df['Time']=pd.to_datetime(df['Time'])
#     df.set_index('Time',inplace=True)
#     time_variables(df)
#     if str(xv)=='weekday':
#         dff=df.resample('1D').sum()
#     if str(xv)=='month':
#         dff=df.resample('1M').sum()
#     if str(xv)=='season':
#         dff=df[list(col)+['season','year']].groupby(['season','year']).sum()
#         dff=dff.reset_index()
#     else:
#         dff=df.copy()
#     fig=px.box(dff, x=str(xv), y=str(yv))
#     return fig
@dash_app.callback(
    Output('graph_boxx', 'figure'),
    Output('graph_mean', 'figure'),
    Input('y-axis', 'value'),
    Input('x-axis', 'value'),
    Input('stored-conscol', 'data'),
    Input('stored-data', 'data'))
def update_figure(yv,xv,col,data):
    col=pd.DataFrame(col)["0"].values.tolist()
    df=pd.DataFrame(data)
    df['Time']=pd.to_datetime(df['Time'])
    df.set_index('Time',inplace=True)
    time_variables(df)
    if str(xv)=='weekday':
        dff=df.resample('1D').sum()
    if str(xv)=='month':
        dff=df.resample('1M').sum()
    if str(xv)=='season':
        dff=df[list(col)+['season','year']].groupby(['season','year']).sum()
        dff=dff.reset_index()
    else:
        dff=df.copy()
    figg= plt.figure(figsize=(28,6))
    ax= figg.add_subplot(111)
    fig=px.box(dff, x=str(xv), y=str(yv))
    sns.lineplot(x=dff[str(xv)], y=dff[str(yv)],ci=None,estimator='mean', hue=dff['year'],ax=ax)
    ax.grid(True)
    plotly_fig = mpl_to_plotly(figg)
    

    
    return fig,plotly_fig

# @dash_app.callback(
#     Output('graph_moy', 'figure'),
#     Input('stored-data', 'data'),
#     Input('stored-conscol', 'data'))
# def update_figure2(data,col):
#     df=pd.DataFrame(data).set_index('Time')
#     col=pd.DataFrame(col)["0"].values.tolist()
#     coll=[c for c in list(df.columns) if c not in col]
#     fig2=px.line(df[coll])
#     fig2.update_xaxes(rangeslider_visible=True)
#     fig2.for_each_trace(lambda trace: trace.update(visible="legendonly") 
#                     if trace.name in coll else ())
#     return fig2

# @dash_app.callback(
#     Output('page-2-display-value', 'children'),
#     Input('page-2-dropdown', 'value'))
# def display_value(value):
#     return f'You have selected {value}'


