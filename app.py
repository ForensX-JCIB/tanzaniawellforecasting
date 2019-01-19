import dash
colorscale = {
    
}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://codepen.io/amyoshino/pen/jzXypZ.css',
                        "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css",
                        "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",  # Normalize the CSS
                        "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css",
                        "https://fonts.googleapis.com/css?family=Open+Sans|Roboto"  # Fonts
                        "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                        "https://cdn.rawgit.com/TahiriNadia/styles/faf8c1c3/stylesheet.css",
                        "https://cdn.rawgit.com/TahiriNadia/styles/b1026938/custum-styles_phyloapp.css",
                        "https://cdn.rawgit.com/chriddyp/0247653a7c52feb4c48437e1c1837f75/raw/a68333b876edaf62df2efa7bac0e9b3613258851/dash.css"
                        ]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Well Forecasting"
server = app.server
app.config.suppress_callback_exceptions = True