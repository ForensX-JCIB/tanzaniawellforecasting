import dash_html_components as html
import dash_core_components as dcc

import dash_html_components as html
import dash_core_components as dcc

from apps.Components import colorscale

##LOGO FOR THE APP
logoLink = 'http://p10cdn4static.sharpschool.com/UserFiles/Servers/Server_109143/Image/Logo/JCIB-Logo-Website.png'
def Header():
    return html.Div([
        get_logo(),
        get_header(),
    ])

def get_logo():

    logo = html.Div(
        className = 'jcib-logo',
        children=[
            html.Img(src=logoLink, height='80', width='80')
        ]
    )

    return logo

def get_header():
    header=html.Div(
        className='row',
        style={
            'margin-left':'0px',
            'margin-right':'0px',
            'background-color':colorscale.navBG,
            'height':100,
            'margin-bottom':'25px',
        },
        children=[
            #html.H5('Tanzanian Water Wells: Analytics and Machine Learning-based Forecasting', style={'color':colorscale.navText, 'padding': '20px 0px', 'font-size':'35px'}),
            html.H5('Water Well Analytics: Tanzania', className='website-title'),
            get_menu(),
        ]
    )
    return header


def get_menu():
    menu = html.Div(
        className='navbar-blue-pills',
        children=[
            dcc.Link('Home', href='/', className="active"),

            dcc.Link('Analysis', href='/apps/analysis'),

            dcc.Link('Machine Learning', href='/apps/machinelearning'),

            dcc.Link('Forecast', href='/apps/uploaddata'),
        ], 
    )
    return menu
