import base64
import datetime
import io

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib

from app import app
from apps.Components import header

#color scheme
from apps.Components import colorscale

lonnie_forecast_model = joblib.load('Master Data//lonnie_joblib_forecasting.joblib')

mapbox_access_token = "pk.eyJ1IjoicGFudDIwMDIiLCJhIjoiY2prenlwb2ZtMHlnMjNxbW1ld3VxYWZ4cCJ9.rOb8DhCzsysBIw69MxyWKg"

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def process_for_forecasting(df, model = lonnie_forecast_model):
    df['date_recorded'] = pd.to_datetime(df['date_recorded'])
    df['month_recorded'] = df['date_recorded'].dt.month
    df['year_recorded'] = df['date_recorded'].dt.year
    nonzero_mean = df.loc[df.construction_year != 0,'construction_year' ].mean()
    nonzero_mean = int(round(nonzero_mean))
    df.loc[ df.construction_year == 0, "construction_year" ] = nonzero_mean
    df['age'] = df['year_recorded']- df['construction_year']
    df=df.dropna()
    lf = df.select_dtypes(include="object")
    le = LabelEncoder()
    lf = lf.apply(LabelEncoder().fit_transform)
    dfle = lf.join(df.select_dtypes(exclude="object"))
    X = dfle[['installer', 'basin', 'subvillage', 'region', 'lga', 'ward',
            'public_meeting', 'scheme_management', 'extraction_type', 'management',
            'water_quality', 'quantity', 'source', 'waterpoint_type', 'amount_tsh',
            'gps_height', 'longitude', 'latitude', 'population',
            'construction_year', 'month_recorded', 'year_recorded', 'age']]
    preds = model.predict(X)
    predictions_counts = pd.DataFrame()
    predictions_counts['date_recorded'] = df['year_recorded']
    predictions_counts['forecast'] = preds
    predictions_timeseries = pd.crosstab(predictions_counts['date_recorded'], predictions_counts['forecast'])
    predictions_timeseries.columns = ['Functional', 'Non Functional', 'Functional: Needs Repair']
    predictions_timeseries['Total'] = predictions_timeseries["Functional"] + predictions_timeseries["Non Functional"] + predictions_timeseries["Functional: Needs Repair"]
    return df, dfle, preds, predictions_timeseries





layout = html.Div([
    html.Div(
        className='container',
        style={
            'background-color': colorscale.divBG,
            'text-align':'center',
            'margin-left': 'auto',
            'margin-right': 'auto',
            'display': 'inline',
        },
        children=[
            html.H4("Upload files to get predictions on your own data!")
        ]
    ),
    
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})
])


def parse_contents(contents, filename, date, model = lonnie_forecast_model):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    le = LabelEncoder()
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            df, dfle, preds, predictions_timeseries = process_for_forecasting(df, model = lonnie_forecast_model)

        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            df, dfle, preds, predictions_timeseries = process_for_forecasting(df, model = lonnie_forecast_model)
            
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])


    return html.Div(
        style={

        },
        children=[
            
            html.Div(
                style={
                    'margin-left':'25px',
                    'margin-right':'25px',
                },
                children=[
                    html.H5(filename),
                    #html.H6(datetime.datetime.fromtimestamp(date)),
                ]
            ),

            # Use the DataTable prototype component:
            # github.com/plotly/dash-table-experiments
            html.Div(
                style={
                    'margin-left':'25px',
                    'margin-right':'25px',
                    'margin-bottom':'50px',
                },
                children=[
                    dt.DataTable(rows=df.sample(n=500).to_dict('records')),
                ]
            ),
            html.Div(
                style={
                    'margin-bottom':'25px',
                    'margin-left':'25px',
                    'margin-right':'25px',
                },
                children=[
                    html.Div(
                        style={
                            # 'margin-left':'25px',
                            #'margin-right':'10px',
                            'margin-bottom':'20px',
                        },
                        children=[
                            dcc.Graph(
                                id = 'user-geospatial-forecast',
                                figure={
                                    'data': [
                                        {
                                            "type": "scattermapbox",
                                            "lat": df['latitude'],
                                            "lon": df['longitude'],
                                            "text": df['wpt_name'],
                                            "mode": "markers",
                                            "marker": {
                                                'size': 8,
                                                "colorscale":"Viridis",
                                                "color": preds,
                                                "colorbar" : {
                                                    "thickness" : 10,
                                                    "ticks" : "outside",
                                                    "title":"<b>Water Quality</b><br></br>",
                                                    #'tickmode':'array',
                                                    'tickvals':[0, 1, 2],
                                                    'ticktext': ['Functional', 'Non-Functional', 'Functional: Needs Repair'],
                                                },
                                                "opacity": 0.8,
                                                            
                                            },
                                        },
                                    ],
                                    'layout': 
                                    {
                                        'title': 'Well Status Forecast: Geospatial Analysis',
                                        'height':900,
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
                        ]
                    ),
                    html.Div(
                        style={
                            'margin-top':'20px',
                            # 'margin-left':'10px',
                            #'margin-right':'25px',
                        },
                        children=[
                            dcc.Graph(
                                    id='time-series-user-forecast',
                                    figure={
                                        'data':
                                        [
                                            {
                                                'x':predictions_timeseries.index,
                                                'y':np.cumsum(predictions_timeseries['Functional']),
                                                'name':'Functional',
                                                'type':'Scatter'
                                            },
                                            {
                                                'x':predictions_timeseries.index,
                                                'y':np.cumsum(predictions_timeseries['Non Functional']),
                                                'name':'Non Functional',
                                                'type':'Scatter'
                                            },
                                            {
                                                'x':predictions_timeseries.index,
                                                'y':np.cumsum(predictions_timeseries['Functional: Needs Repair']),
                                                'name':'Functional: Needs Repair',
                                                'type':'Scatter'
                                            },
                                            {
                                                'x':predictions_timeseries.index,
                                                'y':np.cumsum(predictions_timeseries['Total']),
                                                'name':'Total',
                                                'type':'Scatter'
                                            }
                                        ],
                                        'layout':
                                        {
                                            'title':'Time Series Forecasting Of Functionality of Wells',
                                            'xaxis':{
                                                'showgrid':False
                                            },
                                            'height': 900,
                                            "autosize" : True,
                                            'paper_bgcolor': colorscale.divBG,
                                            'plot_bgcolor': colorscale.divBG
                                        }
                                }
                            )
                        ]
                    )
                ]
            )
        ]
    )



@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children



if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)