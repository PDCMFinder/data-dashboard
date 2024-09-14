import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from src.components.util import generate_metadata_score_bar_plot
from src.components.table.elements import score_table_component
from src.assets.resources import labels
from urllib.parse import urlparse, parse_qs
from src.components.navbar.navbar import navbar
from src.components.bar.elements import *
from src.components.table.tables import *

padding = "0.1%"
margin_left = '0.1%'
margin_bottom = "0.1%"
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    navbar(),
    html.Div(children=[
            dcc.Markdown('### Select Data release: ', style={'display': 'inline-block', 'padding-left': '1%', 'margin': '0',
                            'fontSize': '18px', 'fontWeight': 'bold', 'color': '#013e48'}),
            dcc.Dropdown(
                id='ms-dropdown-category',
                options=[{'label': str(labels[category]).title(), 'value': category} for category in
                         labels.keys()],
                value=list(labels.keys())[0],
                multi=False,
                style={'width': '50%', 'display': 'inline-block', 'marginLeft': margin_left, 'fontSize': '16px'}
            )], style={'width': '100%', 'display': 'inline-block', 'display': 'flex', 'alignItems': 'center', 'gap': '2px',
                       'padding': '1px 0', 'backgroundColor': '#f2f2f2', 'border': '1px solid #ddd', 'borderRadius': '8px',
                       'margin-bottom': margin_bottom}),
    #ui_ms_bar_component(),
    ui_ms_bar_plot_component('pdx'),
    ui_ms_bar_plot_component('cell-line'),
    ui_ms_bar_plot_component('organoid'),
    score_table_component()
    ],
    style={'font-family': 'Merriweather', 'padding': padding}
)


def register_callbacks(app):
    @app.callback(
            Output('ms-dropdown-category', 'value'),
            [Input('url', 'href')]
    )
    def set_dropdown_value(href):
        # Parse the URL to get query parameters
        if href:
            parsed_url = urlparse(href)
            query_params = parse_qs(parsed_url.query)
            # Extract filter value from query params
            filter_value = query_params.get('dropdown-category', [None])[0]
            if filter_value in labels.keys():
                return filter_value
        return list(labels.keys())[0]

    @app.callback(
        Output('pdx-model-type-plot', 'figure'),
        [Input('ms-dropdown-category', 'value')]
    )
    def update_pdx_ms_plot(category):
        return generate_metadata_score_bar_plot(category, 'pdx')

    @app.callback(
        Output('cell-line-model-type-plot', 'figure'),
        [Input('ms-dropdown-category', 'value')]
    )
    def update_cell_ms_plot(category):
        return generate_metadata_score_bar_plot(category, 'cell line')

    @app.callback(
        Output('organoid-model-type-plot', 'figure'),
        [Input('ms-dropdown-category', 'value')]
    )
    def update_organoid_ms_plot(category):
        return generate_metadata_score_bar_plot(category, 'organoid')

    @app.callback(
        Output('data-table-ms', 'data'),
        [Input('ms-dropdown-category', 'value')]
    )
    def update_ms_table(category):
        return get_ms_table().to_dict('records')