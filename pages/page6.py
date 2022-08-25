# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 14:19:58 2022

@author: JOUNAIDI
"""
import matplotlib.pyplot as plt

from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np
import pandas as pd
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.tools import mpl_to_plotly

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
    html.H4('Correlation de Pearson'),
    dcc.Graph(id='corr_map'),
    html.H4('Nuage de points'),
    html.H6('Choix des variables :'),
    html.P('axe des x :'),
    dcc.RadioItems(
        id='x-axis_cl', 
        inline=True
    ),
    html.P(' '),
    html.P('axe des y :'),
    dcc.RadioItems(
        id='y-axis_cl', 
        # options=['Socket', 'Light'],
        # value=False, 
        inline=True
    ),
    dcc.Graph(id='cloud_pt'),
])


@dash_app.callback(
    Output('corr_map', 'figure'),
    Input('stored-data', 'data'))
def update_corr(data):
    df=pd.DataFrame(data)
    df['Time']=pd.to_datetime(df['Time'])
    df.set_index('Time',inplace=True)
    # time_variables(df)    
    fig=px.imshow(df.corr(),text_auto=True)

    #fig = go.Figure(data=go.Heatmap(z=ddd, x=list(xTickLabels),y=list(yTickLabels['date'])))
    fig.update_layout(width=1600,height=1000,margin=dict(l=20, r=20, t=20, b=20),)
    return fig



@dash_app.callback(
    Output('x-axis_cl', 'options'),
    Output('y-axis_cl', 'options'),
    Input('stored-data', 'data'))
def update_corr(data):
    df=pd.DataFrame(data)
    df['Time']=pd.to_datetime(df['Time'])
    df.set_index('Time',inplace=True)
    # time_variables(df)    
    c=list(df.columns)
    return c,c

@dash_app.callback(
    Output('cloud_pt', 'figure'),
    Input('x-axis_cl', 'value'),
    Input('y-axis_cl', 'value'),
    Input('stored-data', 'data'))
def update_corr(x,y,data):
    df=pd.DataFrame(data)
    df['Time']=pd.to_datetime(df['Time'])
    df.set_index('Time',inplace=True)
    # time_variables(df)    
    fig = px.scatter(df, x, y)

    #fig = go.Figure(data=go.Heatmap(z=ddd, x=list(xTickLabels),y=list(yTickLabels['date'])))
    fig.update_layout(width=1600,height=1000,margin=dict(l=20, r=20, t=20, b=20),)
    return fig
# @dash_app.callback(
#     Output('graph_pie', 'figure'),
#     Input('my-date-picker-range', 'start_date'),
#     Input('my-date-picker-range', 'end_date'),
#     Input('stored-data', 'data'),
#     Input('stored-conscol', 'data'))
# def update_figure2(st,et,data,col):
#     df=pd.DataFrame(data)
#     df['Time']=pd.to_datetime(df['Time'])
#     df.set_index('Time',inplace=True)
#     time_variables(df)
#     col=pd.DataFrame(col)["0"].values.tolist()
#     dd=df.loc[st:et,col].sum(axis=0)
#         #fig=px.box(df, x="hour", y=col[3])
#     fig = go.Figure(data=[go.Pie(labels=col, values=dd.values,hole=.3)])

# # Change the bar mode
#     fig.update_layout()
    
#     return fig

# def bar_plot_total(df,titre,last_index,first_index=0,ylabel="Wh"):
    
#     plt.figure(figsize=(20,8))
#     dd=df[list(conso_columns)+['month']].groupby('month').sum()
#     dd['Month']=dd.index
#     B=[]
#     plt.title(titre)
#     plt.ylabel(ylabel)
#     b= plt.bar(dd['Month'], dd[list(conso_columns)[first_index]], width = 0.6)
#     B.append(b)
#     S=dd[list(conso_columns)[first_index]]
#     for i,col in enumerate(conso_columns[1:last_index]):
#         b = plt.bar(dd['Month'], dd[col], bottom=S, width = 0.6)
#         S=S+dd[col]
#         B.append(b)
#     plt.legend( B, conso_columns )
#     plt.show()
    

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


