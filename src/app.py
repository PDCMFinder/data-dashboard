from dash import Dash, dcc, html
import src.index as index

app = Dash(__name__, suppress_callback_exceptions=True)

# Setup server for deployment
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
    ], style={'font-family': 'Arial, sans-serif'}
)

index.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
