from flask import Flask
from dash import Dash

import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dtable
from dash.dependencies import Input, Output

from app import app
import os
from apps.Components import header

from sklearn.externals import joblib
import calendar
import pickle
from  datetime import datetime as dt
# AFTER SPENDING AN HOUR, I REALIZED MAPBOX MUST BE USED WITH OLD DASH SYNTAX, NOT NEW PLOTLY SYNTAX. DONT USE A PLOTLY CHLOROPLETH HERE, USE DICTIONARY FORMAT.

import plotly.graph_objs as go

import pandas as pd
import numpy as np

#color sceme
from apps.Components import colorscale

# dataset imports
# Stock Master dataset for audience (non LE)
dfO = pd.read_csv('Master Data//MASTER_Original_Set.csv')
dfO = dfO.drop(['Unnamed: 40', 'id.1', 'id'], axis = 1)
df2018 = pd.read_csv('Master Data//2018_forecast_results.csv')
# Aniket RFC Importances
rfcImportances = pd.read_csv('Master Data//feature_importances.csv')
rfcImportances = rfcImportances.sort_values(by='Importances', ascending = 0)
# Time Series Graph: ML forecast only. Includes geospatial data too
mlForecast = pd.read_csv('Master Data//forecast_geospatial.csv')
mlForecast['date_recorded'] = pd.to_datetime(mlForecast['date_recorded'])
mlForecast_time = mlForecast.sort_values('date_recorded')
status_count_ML = pd.crosstab(mlForecast_time["date_recorded"], mlForecast_time['forecast'])
status_count_ML["Sum"] = status_count_ML.sum(axis=1)
#status_count_ML=status_count_ML.sort_values(by=["Sum"],ascending=False)
status_count_ML = status_count_ML.drop(status_count_ML.index[[list(range(0, 12))]])
status_count_ML.columns = ['Functional', 'Non-Functional', 'Functional: Needs Repair', 'Total']
# TEST SET FOR FORECAST RESULTS
testSet = pd.read_csv("Master Data//TEST_label_encoded.csv", parse_dates=True)
testSet['construction_year'] = pd.to_datetime(testSet['construction_year'], utc=True)
testSet['construction_year'] = testSet['construction_year'].dt.year
###Time series stuff with stuff####
orig = pd.read_csv('Master Data//MASTER_Original_Set.csv')
forecastdf = pd.read_csv("Master Data//label_encoded.csv")
lonnie_forecast_model = joblib.load('Master Data//lonnie_joblib_forecasting.joblib')

def lonnie_forecast_function(input_date, orig = orig, forecastdf = forecastdf, forecast_model = lonnie_forecast_model):
    forecastdf['date_recorded'] = pd.to_datetime(input_date)
    forecastdf['month_recorded'] = forecastdf['date_recorded'].dt.month
    forecastdf['year_recorded'] = forecastdf['date_recorded'].dt.year
    nonzero_mean = forecastdf.loc[forecastdf.construction_year != 0,'construction_year' ].mean()
    nonzero_mean = int(round(nonzero_mean))
    forecastdf.loc[ forecastdf.construction_year == 0, "construction_year" ] = nonzero_mean
    forecastdf['age'] = forecastdf['year_recorded']- forecastdf['construction_year']   
    dftodrop = ['id.1', 'id', 'district_code', 'date_recorded', 'funder', 'num_private', 'payment', 'recorded_by', 'region_code', 'permit','wpt_name', 'scheme_name', 'extraction_type_group', 'quantity_group', 'waterpoint_type_group', 'quality_group', 'source_type', 'management_group', 'extraction_type_class', 'source_class', 'payment_type','status_group']
    new_wells_forecast_ML = forecastdf.drop(dftodrop, axis = 1)
    year_forecast = lonnie_forecast_model.predict(new_wells_forecast_ML)
    return year_forecast
#######################################

# MAPBOX TOKEN
mapbox_access_token = "pk.eyJ1IjoicGFudDIwMDIiLCJhIjoiY2prenlwb2ZtMHlnMjNxbW1ld3VxYWZ4cCJ9.rOb8DhCzsysBIw69MxyWKg"


MLlayout = html.Div(
    style={
        'display':'flex-inline',
        'flex-direction':'column',
        'justify-content':'space-between',
        'margin-right':'30px',
        'margin-left':'30px',
        'margin-bottom':'30px',
    },
    children=[
    html.Div([
        html.Div(
            style={
                'display':'flex',
                'flex-direction':'row',
                'margin-bottom':'20px',
            },
            children=[
                html.Div(children = [
                        html.Div(
                            style={
                                'margin-left':'2%',
                                'margin-right':'2%',
                            },
                            children = [
                                html.H1('Machine Learning', style={'font-weight':'bold', 'font-size':'30px',}),
                                html.P('This app possesses the ability to forecast the status of individual wells at any given date in time. We believe this allows engineers and social workers to find problematic wells soon in need of repair before a problem occurs. Users simply scroll down, select a date, and the model predicts the functionality of each well at the given date.', className='ml-textbox list-group-item'),
                                html.P('Our model can capture the effect of seasonality, location, and all of the given variables in the data sample. Our model can perform predictions with an accuracy of 81%.', className='ml-textbox list-group-item'),
                                html.P('Additionally, since we elected to use a Random Forest, we had the ability to estimate variable importances. Essentially, we are evaluating what variables contribute most to the observed functionality of the well (functioning, nonfunctioning, needs repair).',className='ml-textbox list-group-item'),
                                html.H1('Findings:', style={'font-weight':'bold', 'font-size':'28px', 'margin-top':'3%'}),
                                html.P('The quantity of water available in the well and the location of the well were the most important factors in functionality determination.', className='ml-textbox list-group-item')
                            ]
                        ),
                        
                        ], 
                        style={
                            'background-color': colorscale.divBG,
                            'height':'650px',
                            'flex':'1',
                            'margin-right':'20px',
                        },
                ),

                html.Div([
                    html.Div(
                        style={
                            'margin-left':'40px',
                            'margin-right':'40px',
                        },
                        children=[
                            html.H3("Data Sample"),
                            html.P("Presented below is data used to train our Machine Learning model, as well as the functionality of the recorded pump."),
                            html.P("A sample of 500 records are shown here. Approximately 60,000 records are used to train the predictive model."),
                            dtable.DataTable(
                                rows=dfO.sample(n=500).to_dict('records'),
                                columns=dfO.columns,
                                row_selectable=False,
                                filterable=True,
                                sortable=True,
                                selected_row_indices=[],
                                id='data_sample_table'
                            ), 
                        ]
                    ),
                    
                    ], 
                    style={
                        'background-color':colorscale.divBG,
                        'flex':'3',
                        'margin-left':'20px',
                    }
                )
            ],
        ),
        html.Div(
            style={
                'display':'flex',
                'flex-direction':'row',
                'margin-bottom':'20px',
                'margin-top':'20px',
            },
            children=[
                html.Div(
                    style = {
                        
                    },
                    children=[
                        html.Div(
                            style={
                                'flex':'1',
                                'background-color':colorscale.divBG,
                                'margin-right':'20px',
                            },
                            children=[
                                dcc.Graph(
                                    figure=go.Figure(
                                        data=[
                                            go.Bar(
                                                y = rfcImportances['Variable'][0:10],
                                                x = rfcImportances['Importances'][0:10],
                                                orientation='h'
                                            )
                                        ],
                                        layout=go.Layout(
                                            title='Random Forest Classifier: Relative Importances',
                                            height = 650,
                                            paper_bgcolor = colorscale.divBG,
                                            plot_bgcolor = colorscale.divBG
                                        )
                                    ),
                                    id='rfc-feature-importances'
                                )
                            ]
                        )
                    ],
                ),
                html.Div(
                    style={
                        'flex':'1',
                        'background-color':colorscale.divBG,
                        'margin-left':'20px',
                    },
                    children = [
                        #Begin Geospatial Forecast 
                html.Div(
                    style={
                        'height': '600px',
                        'width':'100%'
                    },
                    children=[
                        dcc.DatePickerSingle(
                            min_date_allowed=dt(1995, 8, 5),
                            max_date_allowed=dt(2020, 9, 19),
                            initial_visible_month=dt(2018, 10, 16),
                            #date=dt(2017, 8, 25),
                            id='user-forecasting-date',
                        ),
                        dcc.Graph(
                            id='mapbox-lonnie_forecast',
                            figure={
                                'data':[
                                    {    
                                        'type': 'scattermapbox',
                                        'lat': df2018['latitude'],
                                        'lon': df2018['longitude'],
                                        'mode': 'markers',
                                        'opacity': 0.4,
                                        'marker': {
                                            'size': 9,
                                            'color': df2018['2018_forecast'],
                                            'colorbar': {
                                                'title': '<b>Well Status</b>',
                                                'titleside': 'top',
                                                'tickmode': 'array',
                                                'tickvals': [0, 1, 2],
                                                'ticktext': ['Functional','Non-functional','Functional Needs Repair'],
                                                'ticks': 'outside',
                                            },
                                            'colorscale':'Viridis',
                                        }
                                    }
                                ],
                                'layout': {
                                    'height': 600,
                                    'title': "2018 Water Well Functionality Status Forecast",
                                    'hovermode': 'closest',
                                    'mapbox': {
                                        'accesstoken': mapbox_access_token,
                                        'bearing': 0,
                                        'center':{
                                            'lat': -6.3,
                                            'lon': 36,
                                        },
                                        'pitch': 0,
                                        'zoom': 4.2,
                                        'style': 'satellite-streets',
                                    },
                                    'paper_bgcolor': colorscale.divBG,
                                    'plot_bgcolor': colorscale.divBG,
                                }
                            },
                        ),
                ]
                ),
                #End Geospatial Forecast  
                    ],
                ),
            ]
        ),
    ])
])

 
@app.callback(
    Output(component_id='mapbox-lonnie_forecast', component_property='figure'),
    [Input(component_id='user-forecasting-date', component_property='date')])
def update_geospatial_forecast(date):

    if date is not None:
        date = dt.strptime(date, '%Y-%m-%d')
    
    month = date.month
    month_name = calendar.month_name[month]
    year = date.year

    geo_forecast = lonnie_forecast_function(date, orig = orig, forecastdf = forecastdf, forecast_model = lonnie_forecast_model)
    return ({
                        'data': [
                                {
                                "type": "scattermapbox",
                                    "lat": forecastdf['latitude'],
                                    "lon": forecastdf['longitude'],
                                    "text": geo_forecast,
                                    "mode": "markers",
                                    "marker": {
                                        "colorscale":"Viridis",
                                        "color": geo_forecast,
                                        "colorbar" : {
                                            "thickness" : 10,
                                            "ticks" : "outside",
                                            "title":"<b>Well Functionality</b><br></br>",
                                            #'tickmode':'array',
                                            'tickvals':[0,1,2],
                                            'ticktext': ['Functional', 'Non-Functional', 'Needs Repair'],

                                        },
                                        "opacity": 0.8,
                                          
                                    },
                                },
                            ],
                            'layout': {
                                'title': '{}, {} Forecast: Geospatial Analysis'.format(month_name, year),
                                'height': 600,
                                "autosize" : True,
                                "hovermode": "closest",
                                "mapbox": {
                                    "accesstoken" : mapbox_access_token,
                                    "bearing": 0,
                                    "center": {
                                        "lat" : -6.3,
                                        "lon" : 36
                                    },
                                    "pitch" : 0,
                                    "style" : 'satellite-streets',
                                    "zoom" : 6
                                },
                                'paper_bgcolor': colorscale.divBG,
                                'plot_bgcolor': colorscale.divBG

                            }
        })

