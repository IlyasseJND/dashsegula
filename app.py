# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 03:20:07 2022

@author: Admin
"""

from dash import Dash, dcc, html, Input, Output, callback, dash_table
from pages import page1, page2, page3,page4,page5,page6
import dash_bootstrap_components as dbc
# Importation des bibliothéque
import os
import plotly.graph_objects as go

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
# premier fichier 'Consommation_energie.csv'
df_consom=pd.read_csv(r'dataset/Cons_energie.csv',header=0,parse_dates=['Time'],index_col='Time')
col_cons=list(df_consom.columns)

df_temp0=pd.read_csv(r'dataset/Température_chambre_principale.csv',header=0,parse_dates=['Time'],index_col='Time')
df_temp1=pd.read_csv(r'dataset/Température_chambre_supplémentaire.csv',header=0,parse_dates=['Time'],index_col='Time')
df_temp2=pd.read_csv(r'dataset/Température_salle_travail.csv',header=0,parse_dates=['Time'],index_col='Time')
dt=df_consom.index[1]-df_consom.index[0]
dt=dt.seconds/60
df_cons=df_consom.resample('H').sum()*dt/60
df1=pd.merge(df_cons,df_temp0,how='left',left_on='Time', right_on='Time')
df1=pd.merge(df1,df_temp1,how='left',left_on='Time', right_on='Time')
df1=pd.merge(df1,df_temp2,how='left',left_on='Time', right_on='Time')
path=r'dataset//station/'
filename=os.listdir(path)
df2=pd.read_csv(path+filename[1],parse_dates=['PeriodStart','PeriodEnd'])
df2.drop(['PeriodEnd','Period'],axis=1,inplace=True)
df2['PeriodStart']=df2['PeriodStart'].dt.tz_localize(None)
df2.drop(['GtiFixedTilt','GtiTracking','SnowWater'],axis=1,inplace=True)
dff2=pd.read_csv(path+filename[0],parse_dates=['PeriodStart','PeriodEnd'])
dff2.drop(['PeriodEnd','Period'],axis=1,inplace=True)
dff2['PeriodStart']=dff2['PeriodStart'].dt.tz_localize(None)

dff2=dff2[46:].copy()
#tableau des temperature
ddf2=pd.concat([df2,dff2],axis=0)
df1.reset_index(inplace=True)
df3=pd.merge(df1,ddf2,how="inner",left_on='Time',right_on='PeriodStart')
df3.drop('PeriodStart',axis=1,inplace=True)
#df=df3.set_index('Time')
df=df3.to_dict('records')
col_cons=pd.DataFrame(col_cons).to_dict('records')
#####



dash_app = Dash(__name__,suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.CYBORG])
server = dash_app.server

dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),

dbc.Container([dcc.Store(id="stored-conscol",data=col_cons)]),
dbc.Container([dcc.Store(id="stored-data",data=df)]),
])


Layout=html.Div([
    dbc.Navbar(children=[
        dbc.NavItem(dbc.NavLink(children=dbc.Button("base de données",color="success"), href="/")),
        dbc.NavItem(dbc.NavLink(children=dbc.Button("informations statistiques",color="success"), href="/page1")),
        dbc.NavItem(dbc.NavLink(dbc.Button("Graphes statistique",color="success"), href="/page4")),
        dbc.NavItem(dbc.NavLink(dbc.Button("courbes",color="success"), href="/page2")),
        dbc.NavItem(dbc.NavLink(dbc.Button("comparaisons de consommations",color="success"), href="/page3")),
        dbc.NavItem(dbc.NavLink(dbc.Button("Heatmaps",color="success"), href="/page5")),
        dbc.NavItem(dbc.NavLink(dbc.Button("Correlation",color="success"), href="/page6")),],
         color="primary",),
    html.H2('DashBoard : EDA - Explotory Data Analysis'),
    html.Div([ 
    dbc.Container([dbc.Label('la base de données:'),
                   
    dash_table.DataTable(style_data={
        'color': 'black',
    },
        
        style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold'
    },data=df3.to_dict('records'),
                         columns=[{"name": i, "id": i} for i in df3.columns], id='tbl')]),]),
    ])
    

@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/page1':
        return page1.layout
    elif pathname == '/page2':
        return page2.layout
    elif pathname == '/page3':
        return page3.layout
    elif pathname == '/page4':
        return page4.layout
    elif pathname == '/page5':
        return page5.layout
    elif pathname == '/page6':
        return page6.layout
    else:
        return Layout

if __name__ == '__main__':
    dash_app.run_server(debug=True,port=8000)