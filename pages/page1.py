# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 03:18:32 2022

@author: Admin
"""


from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
# Importation des bibliothéque
import plotly.express as px
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns



#df_stat=df.describe()#faaut partager dataframe between files
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
        
        html.H4('Informations général'),
        html.Div(id='data-size',children=[]),
        html.Div(id='data-col',children=[]),
        
        html.H4('Informations statistique'),
        html.Div(id='data-describe',children=[]),
        
        html.H4('Valeur manquantes'),
        html.Div(id='data-nan',children=[]),
        
    
    ])

@dash_app.callback(
    Output('data-describe', 'children'),
    Input('stored-data', 'data'))
def display_describe(data):
    dff=pd.DataFrame(data)
    T=dff.describe().reset_index()
    
    return dbc.Container([dbc.Label('La description statistique des données:'),
                   
    dash_table.DataTable(T.to_dict('records'),
                         columns=[{"name": i, "id": i} for i in T.columns], id='tbl_desc',style_table={'overflowX': 'auto'},style_data={
        'whiteSpace': 'normal',
        'color': 'black',
    },    style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold'
    })])

@dash_app.callback(
    Output('data-size', 'children'),
    Input('stored-data', 'data'))
def display_size(data):
    s1=pd.DataFrame(data).shape[0],
    s2=pd.DataFrame(data).shape[1],
    return  f'nombre lignes: {s1} ,colonnes : {s2}'

# @dash_app.callback(
#     Output('data-col', 'children'),
#     Input('stored-data', 'data'))
# def display_col(data):
    
#     a=pd.DataFrame(data).count().reset_index()
#     c=pd.concat([pd.DataFrame(pd.DataFrame(data).dtypes).reset_index(),a ],join='inner', axis=1)
#     return  dbc.Container([
#         dash_table.DataTable(c.to_dict('records'),
#                           columns=[{"name": i, "id": i} for i in c.columns], id='tbl_col')])
         

@dash_app.callback(
    Output('data-nan', 'children'),
    Input('stored-data', 'data'))
def display_nan(data):
    s=pd.DataFrame(data).isna().sum().to_frame('nombre de NAN').reset_index()
    return  dbc.Container([dbc.Label('Les valeur manquantes des données:'),
       dash_table.DataTable(style_data={
        'whiteSpace': 'normal',
        'height': 'auto','maxWidth': 1,'lineHeight': '30px','width': '100px','color': 'black',
    },    style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold'
    }
           ,data=s.to_dict('records'),
                         columns=[{"name": i, "id": i} for i in s.columns], id='tbl_na')])




