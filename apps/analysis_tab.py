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

###TIME SERIES###
df_time_unparsed = df[['date_recorded', 'status_group']]
df_time_unparsed['date_recorded'] = pd.to_datetime(
    df_time_unparsed['date_recorded'])
df_time = df_time_unparsed.sort_values('date_recorded')
status_count=pd.crosstab(df_time["date_recorded"], df["status_group"])
status_count["Sum"]=status_count.sum(axis=1)
status_count = status_count.drop(status_count.index[[list(range(0,12))]])
date = status_count.index
functionality_cumsum = np.cumsum(status_count['functional'])

##data processing for time series rangefinder##
dfRange=df[df['status_group'] == 'functional needs repair']
dfRange=dfRange['date_recorded'].value_counts()
dfRange=dfRange.sort_index()
dfRange = dfRange.reset_index()
dfRange.columns = ['date_recorded', 'reports']
dfRange.drop(df.index[0], inplace=True)
################################################


Analysislayout = html.Div(
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
            'height':'700px',
            'background-color':colorscale.bg,
            'display':'flex',
            'flex-direction':'row',
        },
        children=[
            #Begin table of contents
            html.Div(
                style={
                    'background-color':colorscale.bg,
                    'height':700,
                    'flex':'2',
                    'width':'34%',
                    'margin-right':'20px',
                    'flex-direction':'column',
                    'margin-bottom':'20px',
                },
                children=[
                    html.Div(
                        style={
                            'background-color':colorscale.divBG,
                            'flex':1,
                            'flex-direction':'row',
                            'height':'39%',
                            'margin-bottom':'20px',
                        },
                        children=[
                            html.H2(
                                'In our app, we provide analytics on:',
                                style={
                                    'font-size':'35px',
                                    'margin-left':'2%',
                                    'font-weight':'bold',
                                },
                                className='display 4'
                            ),
                            html.Ul(
                                className='list-group list-group-flush',
                                style={
                                    'margin-left':'2%',
                                    'margin-right':'2%',
                                },
                                children=[
                                    html.Li('Geographics', className='analysis-findings list-group-item'),
                                    html.Li('Time Series Progression', className='analysis-findings list-group-item'),
                                    html.Li('Driving factors of well deterioration', className='analysis-findings list-group-item'),
                                    html.Li('Interplay between water quality, geography, and functionality', className='analysis-findings list-group-item'),
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        style={
                            'background-color':colorscale.divBG,
                            'flex':1,
                            'margin-top':'20px',
                            'margin-bottom':'20px',
                            'flex-direction':'row',
                            'height':'58%',
                        },
                        children=[
                            html.Div(
                                style={
                                    'margin-bottom':'10px',
                                },
                                children=[
                                    html.H2(
                                        'Key Findings:',
                                        style={
                                            'font-size':'35px',
                                            'margin-left':'2%',
                                            'font-weight':'bold'
                                        }
                                    ),
                                    html.Ul(
                                        children=[
                                            html.Li('A very large congregation of non-functional wells in the Ruvuma and Southern Coast region. ', className='analysis-findings list-group-item'),
                                            html.Li('In the Southern Coast region, we found a large congregation of "soft" water quality in wells. ', className='analysis-findings list-group-item'),
                                            html.Li('A large percentage of communal wells (wells shared between villages) in the Ruvuma and Southern Coast region, Pangani region, and the Lake Tanganyika region, making these areas of high impact.', className='analysis-findings list-group-item'),
                                            html.Li('We found a strong correlation between salty, abandoned water quality type and wells needing repair. ', className='analysis-findings list-group-item'),
                                        ],
                                    )                                    
                                ]
                            )
                        ]
                    ),
                    
                ]   
            ),
            #End table of contents
            html.Div(
                style={
                    'flex':'3',
                    'width':'40%',
                    'margin-left':'20px',
                    'justify-content':'space-between',
                },
                children=[
                    html.Div(
                        style={
                            'display':'flex',
                        },
                        children=[
                            html.Div(
                                style={
                                    'background-color':colorscale.divBG,
                                    'height':'337px',
                                    'text-align':'center',
                                    'flex':'1',
                                    'margin-right':'20px',
                                },
                                children=[
                                    html.H5('Functioning Water Wells', style={'border-bottom': '2px solid black', 'font-weight': 'bold', 'font-size':'32px'}),
                                    html.H1('12902', style={'font-size':'80px', 'padding':'65px 0', 'color':'#00d600', 'font-weight': 'bold'})
                                ]
                            ),
                            html.Div(
                                style={
                                    'background-color':colorscale.divBG,
                                    'height':'337px',
                                    'text-align':'center',
                                    'flex':'1',
                                    'margin-left':'20px',
                                    'margin-right':'20px',
                                },
                                children=[
                                    html.H5('Wells In Need of Repair', style={'border-bottom': '2px solid black', 'font-weight': 'bold', 'font-size':'32px'}),
                                    html.H1('2142', style={'font-size':'80px', 'padding':'65px 0', 'color':'#ff9966', 'font-weight': 'bold'})
                                ]
                            ),
                            html.Div(
                                style={
                                    'background-color':colorscale.divBG,
                                    'height':'337px',
                                    'text-align':'center',
                                    'flex':'1',
                                    'margin-left':'20px',
                                },
                                children=[
                                    html.H5('Non Functioning Water Wells', style={'border-bottom': '2px solid black', 'font-weight': 'bold', 'font-size':'32px'}),
                                    html.H1('9227', style={'font-size':'80px', 'padding':'65px 0', 'color':'red', 'font-weight': 'bold'})
                                ]
                            ),
                        ]
                    ),
                    html.Div(
                        style={
                            'display':'flex',
                            'margin-top':'25px',
                        },
                        children=[
                            html.Div(
                                style={
                                    'background-color':colorscale.divBG,
                                    'height':'337px',
                                    'text-align':'center',
                                    'flex':'100',
                                    'margin-right':'20px',
                                },
                                children=[
                                    html.H5('Repair Reports in the Last 2 Months', style={'border-bottom': '2px solid black','font-weight':'bold'}),
                                    html.H1('4.67%', style={'font-size':'80px', 'padding':'65px 0', 'color':'#ad1111', 'font-weight': 'bold'})
                                ]
                            ),
                            html.Div(
                                style={
                                    'background-color':colorscale.divBG,
                                    'height':'337px',
                                    'text-align':'center',
                                    'flex':'211',
                                    'margin-left':'20px',
                                },
                                children=[
                                    dcc.Graph(
                                    className='yeet',
                                    style={
                                        'height':'100%'
                                    },
                                        figure={
                                            'data':[
                                                {
                                                    'type':'scatter',
                                                    'x':list(dfRange['date_recorded']),
                                                    'y':list(dfRange['reports']),   
                                                }
                                            ],
                                            'layout':{
                                                'font':{
                                                    'family':'\'Roboto\', sans-serif'
                                                },
                                                'title':'Wells In Need of Repair / Day',
                                                'xaxis':{
                                                    'rangeselector':{
                                                        'buttons':[
                                                            {
                                                                'count':1,
                                                                'label':'1m',
                                                                'step':'month',
                                                                'stepmode':'backward'
                                                            },
                                                            {
                                                                'count':6,
                                                                'label':'6m',
                                                                'step':'month',
                                                                'stepmode':'backward'
                                                            },
                                                            {
                                                                'count':1,
                                                                'label':'YTD',
                                                                'step':'year',
                                                                'stepmode':'todate'
                                                            },
                                                            {
                                                                'count':1,
                                                                'label':'1y',
                                                                'step':'year',
                                                                'stepmode':'backward'
                                                            },
                                                            {
                                                                'step':'all'
                                                            }
                                                        ]
                                                    },
                                                    'rangeslider':{
                                                        'visible':True,
                                                    },
                                                    'type':'date'
                                                },
                                                'yaxis':{
                                                    'title':'Wells Reported In Need of Repairs',
                                                    'font-size':14,
                                                },
                                            }
                                        }
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        ]
    ),
    #End row 1
    #START row 2
    html.Div(
        style={
            'display':'flex',
            'flex-direction':'row',
            'margin-top':'40px',
        }, 
        children = [
            #Begin heatmap
            html.Div(
                style={
                    'height':'650px',
                    'flex':'1',
                    'background-color':colorscale.divBG,
                    'margin-right':'20px',
                },
                children = [
                    html.Div(
                        children=[ # Lake/basin selector
                            dcc.Dropdown(
                                id = 'repair_population_communal_selector',
                                options = [
                                    {'label': 'Well Functionality', 'value': 'Repair'},
                                    {'label': 'Waterpoint Types', 'value': 'Communal_wells'},
                                    {'label': 'Water Quality', 'value': "water_quals"}
                                ],
                                value = 'Repair',
                            )
                        ]
                    ),
                    html.Div(
                        children=[
                            dcc.Graph(id = 'basin_heatmap')
                        ]
                    )
                ],
            ),
            #End heatmap
            #begin geo-spatial of status
            html.Div(
                children=[
                    html.Div(
                        style={
                        },
                        children=[
                            #begin graph
                            dcc.Graph(
                                id='functionality-graph',
                                figure={
                                    'data': [
                                                {
                                                    "type": "scattermapbox",
                                                    "lat": dfLE['latitude'],
                                                    "lon": dfLE['longitude'],
                                                    "text": df["status_group"],
                                                    "mode": "markers",
                                                    "marker": {
                                                        'size': 8,
                                                        "colorscale":"Jet",
                                                        "color": dfLE["status_group"],
                                                        "colorbar" : {
                                                            "thickness" : 10,
                                                            "ticks" : "outside",
                                                            "title": "Well Functionality",
                                                            #'tickmode':'array',
                                                            'tickvals':[0,1,2],
                                                            'ticktext': ["Functional", "Functional: Needs Repair", "Non-Functional"],
                                                        },
                                                        "opacity": 0.8,

                                                    },
                                                },
                                            ],
                                    'layout': {
                                        'font':{
                                            'family':'\'Roboto\', sans-serif'
                                        },
                                        'title': 'Well Functionality: Geospatial Distribution',
                                        'height':650,
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
                                }
                            )   
                            #end graph
                        ]
                    )
                    
                ],
            style={
                'height':650,
                'flex':'1',
                'margin-left':'20px',
            },
        ),
        #End geo-spatial distribution of status
        
    ],),
    #END row 2
    #START row 3
    html.Div(
        style={
            'display':'flex',
            'flex-direction':'row',
            'margin-top':'40px',
        }, 
        children=[
            html.Div(
                style={
                    'height':550,
                    'flex':1,
                    'background-color':colorscale.divBG,
                    'margin-right':'20px',
                },
                children=[
                    dcc.Dropdown(
                        id = 'donut-dropdown',
                        options = [
                            {'label': 'Top 5 Selected by: Functional Wells', 'value': 'functional'},
                            {'label': 'Top 5 Selected by: Non Functional Wells', 'value': 'non functional'},
                            {'label': 'Top 5 Selected by: In Need Of Repair', 'value': 'functional needs repair'}
                        ],
                        value = 'functional',
                    ),
                    dcc.Graph(
                        id='donut-graph'
                    )
                ],
            ),
            html.Div(
                style={
                    'height':550,
                    'flex':1,
                    'background-color':colorscale.divBG,
                    'margin-left':'20px',
                },
                children=[
                    #Begin TIme Series of Well Functionality
                    dcc.Graph(
                        id='time-series-viraj',
                        figure={
                            'data':[
                                {
                                    'x':status_count.index,
                                    'y':np.cumsum(status_count['functional']),
                                    'name':'Functional',
                                    'type':'Scatter'
                                },
                                {
                                    'x':status_count.index,
                                    'y':np.cumsum(status_count['non functional']),
                                    'name':'Non Functional',
                                    'type':'Scatter'
                                },
                                {
                                    'x':status_count.index,
                                    'y':np.cumsum(status_count['functional needs repair']),
                                    'name':'Functional Needs Repair',
                                    'type':'Scatter'
                                },
                                {
                                    'x':status_count.index,
                                    'y':np.cumsum(status_count['Sum']),
                                    'name':'Total',
                                    'type':'Scatter'
                                }
                            ],
                            'layout':{
                                'font':{
                                    'family':'\'Roboto\', sans-serif'
                                },
                                'title':'Reports Received: A Time Series Analysis of Well Functionality',
                                'xaxis':{
                                    'showgrid':False
                                },
                                'height': 550,
                                "autosize" : True,
                                'paper_bgcolor': colorscale.divBG,
                                'plot_bgcolor': colorscale.divBG,
                            }
                        }
                    ),
                    #End Time Series of  Well Functionality
                ],
            )
        ]
    ),
    #END row 3
    #START row 4
    html.Div(
        style={
            'display':'flex',
            'flex-direction':'row',
            'margin-top':'40px',
        }, 
        children=[
            html.Div(
                style={
                    'height':650,
                    'flex':1,
                    'background-color':colorscale.divBG,
                    'margin-right':'20px',
                },
                children=[
                    dcc.Graph(
                        figure={
                            'data': [
                                        {
                                            "type": "scattermapbox",
                                            "lat": dfLE['latitude'],
                                            "lon": dfLE['longitude'],
                                            "text": df['water_quality'],
                                            "mode": "markers",
                                            "marker": {
                                                'size': 8,
                                                "colorscale":"Jet",
                                                "color": dfLE["water_quality"],
                                                "colorbar" : {
                                                    "thickness" : 10,
                                                    "ticks" : "outside",
                                                    "title":"Water Quality",
                                                    #'tickmode':'array',
                                                    'tickvals':[0, 1, 2, 3, 4, 5, 6, 7],
                                                    'ticktext': ["Coloured", "Fluoride", "Fluoride: Abandoned", "Milky", "Salty", "Salty: Abandoned", "Soft", "Unknown"],
                                                },
                                                "opacity": 0.8,

                                            },
                                        },
                                    ],
                            'layout': {
                                'font':{
                                    'family':'\'Roboto\', sans-serif'
                                },
                                'title': 'Water Quality: Geospatial Distribution',
                                'height':650,
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
                        }
                    )
                ],
            ),
            html.Div(
                style={
                    'height':650,
                    'flex':1,
                    'background-color':colorscale.divBG,
                    'margin-left':'20px',
                },
                children=[
                    dcc.Dropdown(
                            id = 'water_qual_functionality_graph_selector',
                            options = [
                                {'label': 'Grouped - Log Scale', 'value': 'group_log'},
                                {'label': 'Grouped - Linear Scale', 'value': 'group_standard'},
                                {'label': 'Stacked - Log Scale', 'value': "stacked_log"},
                                {'label': 'Stacked - Linear Scale', 'value': "stacked_linear"}
                            ],
                            value = 'group_log',
                    ),
                    dcc.Graph(
                        id = 'water_qual_functionality_bargraph'
                    )
                ],
            )
        ]
    ),
    #END row 4
])

@app.callback(
    Output('basin_heatmap', 'figure'),
    [Input("repair_population_communal_selector", "value")]
)
def update_heatmap(repair_population_communal_selector):
    splice_2013 = df[df['date_recorded'].dt.year == 2013]
    if repair_population_communal_selector == "Repair":
        # HEATMAP CODE
        basins_counts = pd.crosstab(splice_2013['basin'], splice_2013['status_group'])
        figure= go.Figure(
                        data=[
                            go.Heatmap(
                                z = basins_counts.values,
                                y = basins_counts.index,
                                x = basins_counts.columns,
                                colorbar = dict(
                                    title = "Amount of Wells",
                                    titleside = "top",
                                    
                                )
                            )
                        ],
                        layout=go.Layout(
                            font = dict(
                                family="\'Roboto\', sans-serif"
                            ),
                            title='Well Functionality type per Basin Source',
                            height=600,
                            yaxis=go.layout.YAxis(
                                automargin=True,
                            ),
                            autosize=True,
                        )
                    )
        return figure
    elif repair_population_communal_selector == "Communal_wells":
        communal_counts = pd.crosstab(splice_2013['basin'], splice_2013['waterpoint_type'])
        figure= go.Figure(
                        data=[
                            go.Heatmap(
                                z = communal_counts.values,
                                y = communal_counts.index,
                                x = communal_counts.columns,
                                colorbar = dict(
                                    title="Amount of Wells",
                                    titleside="top"
                                )
                            )
                        ],
                        layout=go.Layout(
                            font = dict(
                                family="\'Roboto\', sans-serif"
                            ),
                            title='Waterpoint Type per Basin Source',
                            height=600,
                            yaxis=go.layout.YAxis(
                                automargin=True,
                            ),
                            autosize=True,
                        )
                    )
        return figure
    elif repair_population_communal_selector == "water_quals":
        waterquals_counts = pd.crosstab(
            splice_2013['basin'], splice_2013['water_quality'])
        figure = go.Figure(
                        data=[
                            go.Heatmap(
                                z=waterquals_counts.values,
                                y=waterquals_counts.index,
                                x=waterquals_counts.columns,
                                colorbar = dict(
                                    title="Amount of Wells",
                                    titleside="top"
                                )
                            )
                        ],
                        layout=go.Layout(
                            font = dict(
                                family="\'Roboto\', sans-serif"
                            ),
                            title='Water Quality distribution per Basin Source',
                            height=600,
                            yaxis=go.layout.YAxis(
                                automargin=True,
                            ),
                            autosize=True,
                        )
                    )
        return figure

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)

@app.callback(
    Output('donut-graph', 'figure'),
    [Input("donut-dropdown", "value")]
)
def update_donut(status_group):
    #get top 5 villages
    dftemp = df[df['status_group'] == status_group]
    counts = dftemp['subvillage'].value_counts()
    villages = sorted(list(counts.index[0:5]))

    #filter out datasets for each status group with the top 5 wells
    dffiltered = df[df['subvillage'].isin(villages)]
    functional = dffiltered[dffiltered['status_group'] == 'functional']
    nonFunctional = dffiltered[dffiltered['status_group'] == 'non functional']
    needRepair = dffiltered[dffiltered['status_group'] == 'functional needs repair']

    #get counts of wells in each status group per village
    functional = list(functional['subvillage'].value_counts().sort_index())
    nonFunctional = list(nonFunctional['subvillage'].value_counts().sort_index())
    needRepair = list(needRepair['subvillage'].value_counts().sort_index())

    #generate graphs and return
    figure=fig = {
        'data':[
            {
                "values":functional,
                "labels":villages,
                "hoverinfo":"label+percent+value",
                "hole":.6,
                "type":"pie",
                'domain':{'x':[0, 0.30]},
            },
            {
                "values":nonFunctional,
                "labels":villages,
                "name":"Non Functional",
                "hoverinfo":"label+percent+value",
                "hole":.6,
                "type":"pie",
                'domain':{'x':[0.33, 0.66]},
            },
            {
                "values":needRepair,
                "labels":villages,
                "name":"Need Repair",
                "hoverinfo":"label+percent+value",
                "hole":.6,
                "type":"pie",
                'domain':{'x':[0.69, 1]},
            },
            
            
        ],
        'layout':{
            'font':{
                'family':'\'Roboto\', sans-serif'
            },
            "title":"Well Functionality Reports: Top 5 Villages",
            "annotations":[
                {
                    "font":{
                        'size':18,
                    },
                    "showarrow":False,
                    "text":'Functional',
                    'x':0.08,
                    'y':0.5
                },
                {
                    "font":{
                        'size':18,
                    },
                    "showarrow":False,
                    "text":'Non Functional',
                    'x':.49,
                },
                {
                    "font":{
                        'size':18,
                    },
                    "showarrow":False,
                    "text":'Needs Repair',
                    'x':0.925
                },
                
            ]
        }
    }
    return figure

@app.callback(
    Output('water_qual_functionality_bargraph', 'figure'),
    [Input("water_qual_functionality_graph_selector", "value")]
)
def update_bargraph(water_qual_functionality_graph_selector):
    water_quals_functionality = pd.crosstab(df['water_quality'], df['status_group'])
    water_quals_functionality = water_quals_functionality.T
    if water_qual_functionality_graph_selector == "group_log":
        figure= go.Figure(
                            data=[
                                go.Bar(
                                    x=water_quals_functionality.columns,
                                    y=water_quals_functionality.iloc[0],
                                    name = "Functional"
                                ),
                                go.Bar(
                                    x=water_quals_functionality.columns,
                                    y=water_quals_functionality.iloc[1],
                                    name = "In Need of Repair"
                                ),
                                go.Bar(
                                    x=water_quals_functionality.columns,
                                    y=water_quals_functionality.iloc[2],
                                    name = "Non-Functional"
                                ),

                            ],
                            layout=go.Layout(
                                font = dict(
                                    family="\'Roboto\', sans-serif"
                                ),
                                barmode = 'group',
                                title='Water Quality vs. Well Functionality',
                                height=600,
                                autosize=True,
                                xaxis = dict(
                                    title = "Water Quality"
                                ),
                                yaxis = dict(
                                    title = "Number of Wells - log scale",
                                    type = 'log'
                                )
                            )
                        )
        return figure
    elif water_qual_functionality_graph_selector == "group_standard":
        figure= go.Figure(
                            data=[
                                go.Bar(
                                    x=water_quals_functionality.columns,
                                    y=water_quals_functionality.iloc[0],
                                    name = "Functional"
                                ),
                                go.Bar(
                                    x=water_quals_functionality.columns,
                                    y=water_quals_functionality.iloc[1],
                                    name = "In Need of Repair"
                                ),
                                go.Bar(
                                    x=water_quals_functionality.columns,
                                    y=water_quals_functionality.iloc[2],
                                    name = "Non-Functional"
                                ),

                            ],
                            layout=go.Layout(
                                font = dict(
                                    family="\'Roboto\', sans-serif"
                                ),
                                barmode = 'group',
                                title='Water Quality vs. Well Functionality',
                                height=600,
                                autosize=True,
                                xaxis = dict(
                                    title = "Water Quality"
                                ),
                                yaxis = dict(
                                    title = "Number of Wells"
                                )
                            )
                        )
        return figure
    if water_qual_functionality_graph_selector == "stacked_log":
        figure= go.Figure(
                            data=[
                                go.Bar(
                                    x=water_quals_functionality.columns,
                                    y=water_quals_functionality.iloc[0],
                                    name = "Functional"
                                ),
                                go.Bar(
                                    x=water_quals_functionality.columns,
                                    y=water_quals_functionality.iloc[1],
                                    name = "In Need of Repair"
                                ),
                                go.Bar(
                                    x=water_quals_functionality.columns,
                                    y=water_quals_functionality.iloc[2],
                                    name = "Non-Functional"
                                ),

                            ],
                            layout=go.Layout(
                                font = dict(
                                    family="\'Roboto\', sans-serif"
                                ),
                                barmode = 'stack',
                                title='Water Quality vs. Well Functionality',
                                height=600,
                                autosize=True,
                                xaxis = dict(
                                    title = "Water Quality"
                                ),
                                yaxis = dict(
                                    title = "Number of Wells - log scale",
                                    type = 'log'
                                )
                            )
                        )
        return figure
    if water_qual_functionality_graph_selector == "stacked_linear":
        figure= go.Figure(
                            data=[
                                go.Bar(
                                    x=water_quals_functionality.columns,
                                    y=water_quals_functionality.iloc[0],
                                    name = "Functional"
                                ),
                                go.Bar(
                                    x=water_quals_functionality.columns,
                                    y=water_quals_functionality.iloc[1],
                                    name = "In Need of Repair"
                                ),
                                go.Bar(
                                    x=water_quals_functionality.columns,
                                    y=water_quals_functionality.iloc[2],
                                    name = "Non-Functional"
                                ),

                            ],
                            layout=go.Layout(
                                font = dict(
                                    family="\'Roboto\', sans-serif"
                                ),
                                barmode = 'stack',
                                title='Water Quality vs. Well Functionality',
                                height=600,
                                autosize=True,
                                xaxis = dict(
                                    title = "Water Quality"
                                ),
                                yaxis = dict(
                                    title = "Number of Wells"
                                )
                            )
                        )
        return figure

'''
Index(['id', 'amount_tsh', 'date_recorded', 'funder', 'gps_height',
       'installer', 'longitude', 'latitude', 'wpt_name', 'num_private',
       'subvillage', 'region', 'region_code', 'district_code', 'lga', 'ward',
       'population', 'public_meeting', 'recorded_by', 'scheme_management',
       'scheme_name', 'permit', 'construction_year', 'extraction_type',
       'extraction_type_group', 'extraction_type_class', 'management',
       'management_group', 'payment', 'payment_type', 'water_quality',
       'quality_group', 'quantity', 'quantity_group', 'source', 'source_type',
       'source_class', 'waterpoint_type', 'waterpoint_type_group', 'id.1',
       'status_group', 'month_recorded', 'year_recorded', 'age'],
      dtype='object')
'''