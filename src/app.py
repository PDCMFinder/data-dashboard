from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import src.index as index

app = Dash(__name__, suppress_callback_exceptions=True)

# Setup server for deployment
server = app.server
padding = "0.1%"

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
    ], style={'font-family': 'Merriweather', 'padding': padding}
)

index.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
