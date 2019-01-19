from flask import Flask
from dash import Dash

import pandas as pd
import numpy as np 

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app
import os
from apps.Components import header

from apps.Components import colorscale

import dash_table_experiments as dtable 
from sklearn.externals import joblib
import calendar
import pickle
from  datetime import datetime as dt

import plotly.graph_objs as go

#reading data bases
df = pd.read_csv("Master Data//MasterDataSet.csv", parse_dates=True)
df['date_recorded'] = pd.to_datetime(df['date_recorded'])
dfLE = pd.read_csv("Master Data//label_encoded.csv")
dfGDP = pd.read_csv("Master Data//TanzaniaGDP.csv")
forecastCSV = pd.read_csv("Master Data//population_tanzania.csv")
df_HDI = pd.read_csv("Master Data//df_HDI.csv")

mapbox_access_token = "pk.eyJ1IjoicGFudDIwMDIiLCJhIjoiY2prenlwb2ZtMHlnMjNxbW1ld3VxYWZ4cCJ9.rOb8DhCzsysBIw69MxyWKg"

###Data Processing######
corr = df.corr()
water_qual_counts = pd.value_counts(df['water_quality'], sort = True)
###FORCASTING###########

forecastX = np.array(forecastCSV['Year'])
forecastY = np.array(forecastCSV['Population'])
forecastZ = np.polyfit(forecastX, forecastY, 4)

forecast_command = np.poly1d(forecastZ)

forecast_x = np.arange(2017, 2030, 1)
forecast = forecast_command(forecast_x)
#########################

AboutLayout=html.Div(
    style={
        'display':'flex-inline',
        'flex-direction':'column',
        'justify-content':'space-between',
        'margin-right':'30px',
        'margin-left':'30px',
        'margin-bottom':'30px',
    },
    children=[
        #Start Row 1
        html.Div(
            style={
                'background-color':colorscale.bg,
                'display':'flex',
                'flex-direction':'row',
            },
            children=[
                #start text box
                html.Div(
                    style={
                        'flex':'1',
                        'height':'840px',
                        'background-color':colorscale.divBG,
                        'margin-right':'20px',
                    },
                    children=[
                        html.Div(
                            style={
                                'margin-left':'2%',
                                'margin-right':'2%',
                                'display':'flex',
                                'flex-direction':'column',
                            },
                            children=[
                                html.Div(
                                    style={
                                        'order':'2',
                                    },
                                    children=[
                                        html.H1(
                                            'App Overview:',
                                            style={
                                                'font-weight':'bold',
                                            },
                                        ),
                                        html.P(
                                        'In our app, Water Well Analytics: Tanzania, we present analytics and visualizations for the easy assessment of well functionality and driving factors of well degradation and troubled areas in Tanzania.',
                                        className='app-overview list-group-item', 
                                        ),
                                        html.P(
                                        'We employ advanced forecasting techniques to be able to predict when and where a water well will fail before the failure occurs. ',
                                        className='app-overview list-group-item', 
                                        ),
                                        html.P(
                                        'We hope engineers and social workers can apply our dashboard for the optimal selection of high impact target selection for repair, and hope the results of our study aid engineers and social workers in the assessment of high risk areas.',
                                        className='app-overview list-group-item', 
                                        ),  
                                    ]
                                ),
                                html.Div(
                                    style={
                                        'order':'0',
                                    },
                                    children=[
                                        html.H1(
                                            'The Problem:',
                                            style={
                                                'font-weight':'bold',
                                            },
                                        ),
                                        html.P('844 million people around the world lack access to clean water (December 2018). Access to water, according to the UN, is a human right. ',className='problem-textbox list-group-item'),
                                        html.P('Specifically in Tanzania, with a population of 57.31 million (2017) and only 50% of inhabitants with access to improved sources of clean water, the problem for water access has proliferated in the Tanzanian people. With the Tanzanian population forecasted to reach 63.21 million by 2020, the urgency for the remediation of water distribution could result in the difference between life or death. ',className='problem-textbox list-group-item'),
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                #end text box
                #start graphs
                html.Div(
                    style={
                        'flex':'2',
                        'display':'flex',
                        'flex-direction':'column',
                        'margin-left':'20px',
                        'background-color':colorscale.bg
                    },
                    children=[
                        #start top row
                        html.Div(
                            style={
                                'display':'flex',
                                'height':'400px',
                                'background-color': colorscale.bg,
                                'flex-direction':'row',
                                'margin-bottom':'20px',
                            },
                            children=[
                                #start left graph - population
                                html.Div(
                                    style={
                                        'height':'300px',
                                        'background-color': colorscale.divBG,
                                        'margin-right':'20px',
                                        'flex':'1',
                                    },
                                    children=[
                                        dcc.Graph(
                                            id='forecast-plot-1',
                                            figure={
                                                'data':[
                                                    {
                                                    'x': forecastCSV['Year'],
                                                        'y': forecastCSV['Population'],
                                                        'mode':'lines+markers',
                                                        'name': 'Historical: 1960-2017',
                                                        'type': 'line',
                                                    },
                                                    {
                                                        'x': forecast_x,
                                                        'y': forecast,
                                                        'mode':'lines+markers',
                                                        'name': 'Forecast: 2017-2030',
                                                        'type': 'line',
                                                        }
                                                ],
                                                'layout': {
                                                    'height': "400",
                                                    'title': 'Tanzanian Population: 1960-2030',
                                                    'xaxis': {
                                                        "title": "Year",
                                                        "range": [1960, 2030],
                                                        "tickvals": [1960, 1970, 1980, 1990, 2000, 2010, 2020, 2030]
                                                    },
                                                    'yaxis': {
                                                        'title': "Population (millions)"
                                                    },
                                                    'paper_bgcolor': colorscale.divBG,
                                                    'plot_bgcolor': colorscale.divBG
                                                }
                                            }
                                        ),
                                    ],
                                ),
                                #end left grraph - population
                                #start right graph - HDI/GDP
                                html.Div(
                                    style={
                                        'height':'300px',
                                        'background-color': colorscale.divBG,
                                        'margin-left':'20px',
                                        'flex':'1',
                                    },
                                    children=[
                                        dcc.Dropdown(
                                            id='gdp-hdi-selection',
                                            options=[
                                                {'label': 'GDP', 'value': 'GDP'},
                                                {'label': 'UN: HDI', 'value': 'HDI'},
                                            ],
                                            value='GDP',
                                        ),
                                        dcc.Graph(
                                            id='gdp-hdi-graph'  
                                        ),
                                    ]
                                )
                                #end right graph - HDI/GDP
                            ] 
                        ),
                        #end top row
                        #start bottom row - GEO
                        html.Div(
                            style={
                                'display':'flex-inline',
                                'height':'400px',
                                'background-color':colorscale.divBG,
                                'margin-top':'20px',
                                'flex-direction':'row',
                            },
                            children=[
                                html.H6('Tanzanian Population And Well Distribution: Geospatial', style={'text-align':'center','font-size': "22px"}),
                                html.Div(
                                    style={
                                        'margin-left':'2%',
                                    },
                                    children=[
                                        html.Iframe(id='folium-map', srcDoc=open("Dependencies/TanzaniaPopulationMap.html", 'r').read(), width='98%', height='360'),
                                    ]
                                )
                            ]
                        )
                        #end bottom row - GEO
                    ]
                ),
                #end graphs
            ]
        ),
        #End Row 1
    ],
)


#Callback for HDI/GDP graph
@app.callback(
    Output(component_id='gdp-hdi-graph', component_property='figure'),
    [Input(component_id='gdp-hdi-selection', component_property='value')]
)
def callback1(value):
    if (value == 'GDP'):
        return ({
                'data': [
                    {
                        'x': dfGDP['Year'],
                        'y': dfGDP['US Dollars Per Capita'],
                        'mode':'lines',
                        'fill':'tozeroy',
                        'type': 'Scatter',
                        'name':'GDP'
                    },
                ],
                'layout':{
                    'title': 'Tanzania: GDP Per Capita (1988-2017)<br><a href="https://www.cia.gov/library/publications/the-world-factbook/rankorder/2004rank.html">#192/229: Tanzania (CIA Factbook)</a></br>',
                    'height': 365,
                    "autosize" : True,
                    'xaxis': {
                        'title': 'Year'
                    },
                    'yaxis':{
                        'title': 'GDP ($USD)'
                    },
                    'paper_bgcolor': colorscale.divBG,
                    'plot_bgcolor': colorscale.divBG
                }
            }
        )
    if (value == 'HDI'):
            return ({
                'data': [
                    {
                        'x':df_HDI['Year'],
                        'y':df_HDI['HDI'],
                        'mode':'lines',
                        'fill':'tozeroy',
                        'type':'Scatter',
                    }
                ],
                'layout':{
                    'title': 'Tanzania: Human Development Index (1990-2017)<br><a href="http://hdr.undp.org/en/content/human-development-index-hdi">HDI: United Nations</a></br>',
                    'height': 365,
                    "autosize" : True,
                    'xaxis': {
                        'title': 'Year'
                    },
                    'yaxis':{
                        'title': 'HDI'
                    },
                    'paper_bgcolor': colorscale.divBG,
                    'plot_bgcolor': colorscale.divBG
                }
            }
        )
