import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table_experiments as dt

from app import app
from apps import analysis_tab, ml_tab, data_upload, about_tab
from apps.Components import header, colorscale

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://codepen.io/bcd/pen/KQrXdb.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
               "https://codepen.io/bcd/pen/YaXojL.js"]

for js in external_js:
    app.scripts.append_script({"external_url": js})

app.layout = html.Div([
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
    header.Header(),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

@app.callback(Output('page-content', 'children'),
             [Input('url', 'pathname')])
def display_page(pathname):
    if pathname is None:
        return html.Div('''loading...''')
    elif pathname == '/':
        return about_tab.AboutLayout
    elif pathname == '/apps/machinelearning':
        return ml_tab.MLlayout
    elif pathname == '/apps/uploaddata':
        return data_upload.layout
    elif pathname == '/apps/analysis':
        return analysis_tab.Analysislayout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(port=8000, host='127.0.0.1', debug=True, threaded = True)