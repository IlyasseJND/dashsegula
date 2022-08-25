# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 11:40:36 2022

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
    html.H4('Heatmap : selection des variables'),
    dcc.Checklist(id='heatmap_check',inline=True),
    html.Div(id='test',children=[]),
    html.H4('Heatmap pour les jours:'),
    dcc.Graph(id='heatmap_day'),
    html.H4('Heat map pour les heurs:'),
    dcc.Graph(id='heatmap_hour'),
    
])
from datetime import date

@dash_app.callback(
    Output('heatmap_check', 'options'),
    Output('heatmap_check', 'value'),
    Input('stored-conscol', 'data'))
def update_picker(col):
    col=pd.DataFrame(col)["0"].values.tolist()
    return list(col),list(col)

# @dash_app.callback(
#     Output('test', 'children'),
#     Input('heatmap_check', 'value'))
# def update_test(op):
#     return f'You have selected {op}'
import plotly.graph_objects as go
from mpl_toolkits.axes_grid1 import make_axes_locatable

@dash_app.callback(
    Output('heatmap_day', 'figure'),
    Input('heatmap_check', 'value'),
    Input('stored-data', 'data'))
def update_figure1(col,data):
    df=pd.DataFrame(data)
    df['Time']=pd.to_datetime(df['Time'])
    df['Tim']=df['Time'].copy()
    df.set_index('Time',inplace=True)
    # time_variables(df)    
    
    tz=pd.date_range(start =  df.index[0].strftime('%Y-%m-%d'), end = df.index[-1].strftime('%Y-%m-%d'), freq = '4W')
    tdeb=tz[0].strftime('%Y-%m-%d')
    tfinal=tz[-1].strftime('%Y-%m-%d')
    index = (df['Tim'] >= np.datetime64(tdeb)) & (df['Tim'] < np.datetime64(tfinal))
    data=df.loc[index,col].sum(axis=1).resample('D').sum()
    ddd=data.values
    ddd=ddd.reshape((int(len(ddd)/7/4),7*4))

    yTickLabels = pd.DataFrame(data = pd.date_range(start =  tdeb, end = tfinal, freq = '4W'), columns=['datetime'])
    yTickLabels['date'] = yTickLabels['datetime'].apply(lambda x: x.strftime('%Y-%m'))
    s = [['Sun'+str(i), 'Mon'+str(i), 'Tue'+str(i), 'Wed'+str(i), 'Thu'+str(i), 'Fri'+str(i), 'Sat'+str(i)] for i in range(1,5)]
    s=list(np.array(s).flat)
    fig=px.imshow(ddd,x=s,y=yTickLabels['date'].values[:-1],width=900,height=900,color_continuous_scale='RdBu_r' )
    #fig = go.Figure(data=go.Heatmap(z=ddd, x=list(xTickLabels),y=list(yTickLabels['date'])))
    fig.update_layout()
    return fig



@dash_app.callback(
    Output('heatmap_hour', 'figure'),
    Input('heatmap_check', 'value'),
    Input('stored-data', 'data'))
def update_figure2(col,data):
    df=pd.DataFrame(data)
    df['Time']=pd.to_datetime(df['Time'])
    df['Tim']=df['Time'].copy()
    df.set_index('Time',inplace=True)
    # time_variables(df)    
    
    tz=pd.date_range(start =  df.index[0].strftime('%Y-%m-%d'), end = df.index[-1].strftime('%Y-%m-%d'), freq = '4W')
    tdeb=tz[0].strftime('%Y-%m-%d')
    tfinal=tz[-1].strftime('%Y-%m-%d')
    index = (df['Tim'] >= np.datetime64(tdeb)) & (df['Tim'] < np.datetime64(tfinal))
    data=df.loc[index,col].sum(axis=1)
    ddd=data.values
    print(len(ddd)/7/24)
    ddd=ddd.reshape((int(len(ddd)/7/24),7*24))
    
    yTickLabels = pd.DataFrame(data = pd.date_range(start =  tdeb, end = tfinal, freq = '1W'), columns=['datetime'])
    yTickLabels['date'] = yTickLabels['datetime'].apply(lambda x: x.strftime('%Y-%m-%d'))
    s1 = ['Sun ', 'Mon ', 'Tue ', 'Wed ', 'Thu ', 'Fri ', 'Sat ']
    s11=np.repeat(s1,24)
    s2=[str(i)+'h' for i in range(24)]
    s22=np.tile(s2,7)
    xTickLabels = np.char.add(s11, s22)

    fig=px.imshow(ddd,x=xTickLabels ,y=yTickLabels['date'].values[:-1],width=1000,height=1000,color_continuous_scale='RdBu_r' )
    #fig = go.Figure(data=go.Heatmap(z=ddd, x=list(xTickLabels),y=list(yTickLabels['date'])))
    fig.update_layout()
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


