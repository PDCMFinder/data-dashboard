import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
from src.assets.resources import engine, summary, summary_columns
from src.components.navbar.navbar import navbar
from src.components.pages.home import bar_chart, generate_summary_stats, generate_ss_bar_plot

padding = "0.1%"
margin_left = '0.45%'
margin_bottom = "0.5%"
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    navbar(),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[dcc.Graph(id='overview-bar-chart',)], style={'width': '50%', 'float': 'left'}),
            html.Div(children=[
                dcc.Dropdown(
                    id='ss-dropdown-category',
                    options=[{'label': str(category.replace("_", " ").replace(" type ", ": ").replace(" data points", " data").replace("data ", "data: ")).title(), 'value': category} for category in
                             summary_columns if category != "tag" and category != "links" and category != "date"],
                    value=list(summary_columns)[3],
                    multi=False,
                    style={'width': '100%', 'display': 'inline-block'}
                ),
                dcc.Graph(id='summary-stats-bar-chart')
            ], style={'width': '50%', 'float': 'right'}),
            html.Div(children=[
                dcc.Markdown('### Summary Stats:', style={'display': 'inline-block'}),
                dash_table.DataTable(
                    id='summary-stat-table',
                    columns=[
                        {'name': col, 'id': col} if col != 'links' else {'name': col, 'id': col, 'presentation': 'markdown'} for col in list(summary.columns)
                    ],
                    data=summary.to_dict('records'),
                    style_table={'overflow': 'auto'},
                    style_cell={'textAlign': 'left'},
                    style_header={
                            'backgroundColor': 'rgb(210, 210, 210)',
                            'color': 'black',
                            'fontWeight': 'bold'
                        },
                    export_format='xlsx',
                    export_headers='display',
                    ),
                ], style={'width': '100%', 'margin_bottom': margin_bottom}),
                ]),
        ], style={'height': '10%', 'width': '100%'}),
    ], style={'font-family': 'Merriweather', 'padding': padding},

)


def register_callbacks(app):
    @app.callback(
        Output('overview-bar-chart', 'figure'),
        Input('ss-dropdown-category', 'value')

    )
    def update_bar_chart(value):
        return bar_chart(engine)

    @app.callback(
        Output('summary-stat-table', 'data'),
        Input('ss-dropdown-category', 'value')
    )
    def update_summary_stats(category):
        table = generate_summary_stats(engine)
        return table.to_dict('records')

    @app.callback(
        Output('summary-stats-bar-chart', 'figure'),
        Input('ss-dropdown-category', 'value')
    )
    def update_summary_stats(category):
        table = generate_summary_stats(engine)
        return generate_ss_bar_plot(table[['tag', 'date', category]], category)

def create_links(releases):
    return [f"[{release}](/data-release?dropdown-category={release})" for release in releases]
