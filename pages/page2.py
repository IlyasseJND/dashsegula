# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 03:19:15 2022

@author: Admin
"""
import plotly.express as px
import numpy as np
import pandas as pd
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc


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
    html.H4('Graphes de consommations'),
    dcc.Graph(id='graph_conso'),
    html.H4('Graphes des facteurs'),
    dcc.Graph(id='graph_fact'),
    
])

@dash_app.callback(
    Output('graph_conso', 'figure'),
    Input('stored-data', 'data'),
    Input('stored-conscol', 'data'))
def update_figure(data,col):
    df=pd.DataFrame(data).set_index('Time')
    col=pd.DataFrame(col)["0"].values.tolist()
    fig1=px.line(df[col])
    fig1.update_xaxes(rangeslider_visible=True)
    fig1.update_layout(
    yaxis_title="Wh")
    fig1.for_each_trace(lambda trace: trace.update(visible="legendonly") 
                   if trace.name in col else ())
    return fig1

@dash_app.callback(
    Output('graph_fact', 'figure'),
    Input('stored-data', 'data'),
    Input('stored-conscol', 'data'))
def update_figure2(data,col):
    df=pd.DataFrame(data).set_index('Time')
    col=pd.DataFrame(col)["0"].values.tolist()
    coll=[c for c in list(df.columns) if c not in col]
    fig2=px.line(df[coll])
    fig2.update_xaxes(rangeslider_visible=True)
    fig2.for_each_trace(lambda trace: trace.update(visible="legendonly") 
                    if trace.name in coll else ())
    return fig2

@dash_app.callback(
    Output('page-2-display-value', 'children'),
    Input('page-2-dropdown', 'value'))
def display_value(value):
    return f'You have selected {value}'


