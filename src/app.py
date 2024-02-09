import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
from src.util import *
from src.resources import labels, input_file, reactive_categories

app = dash.Dash(__name__)
app.layout = html.Div(
    children=[
        html.H1("CancerModels.Org - Data Overview Dashboard",
                style={'textAlign': 'left', 'marginBottom': 20, 'backgroundColor': '#013e48', 'color': '#ffffff',
                       'padding': '0.1%', 'padding-top': '2%'}),
        html.Div(
            children=[
                dcc.Graph(
                    id='overview-bar-chart',
                    style={'width': '100%'}
                ),
                dcc.Markdown('### Select Data release:'),
                dcc.Dropdown(
                    id='dropdown-category',
                    options=[{'label': str(labels[category]).title(), 'value': category} for category in
                             input_file.keys()],
                    value=list(input_file.keys())[0],
                    multi=False,
                    style={'width': '100%', 'margin': 'left', 'marginTop': 20}
                ),
            ],
            style={'height': '10%', 'width': '100%', 'margin': 'auto', 'marginTop': '-10'}
        ),
        html.Div(
            children=[
                dcc.Graph(
                    id='model-type-plot',
                    style={'width': '100%', 'marginTop': 20}
                ),
            ],
            style={'width': '33%', 'float': 'left', 'marginTop': '5px'}
        ),
        html.Div(
            children=[
                dcc.Graph(
                    id='dto-pie-plot',
                    style={'width': '100%', 'marginTop': 20}
                ),
            ],
            style={'width': '33%', 'float': 'left', 'marginTop': '5px'}
        ),
        html.Div(
            children=[
                dcc.Graph(
                    id='venn-plot',
                ),
                html.Div([
                    dash_table.DataTable(
                        id='table',
                        columns=[
                            {'name': col, 'id': col} for col in list(data.columns)
                        ],
                        data=data.to_dict('records'),
                        style_table={'overflow': 'auto'},
                        style_cell={'textAlign': 'left'},
                    ),
                ],
                    id='table-container',
                ),
            ],
            style={'width': '30%', 'float': 'right', 'margingBottom': '1%'}
        ),
        html.Div(
            children=[
                dcc.Markdown('### Select attributes for comparison:'),
                dcc.Dropdown(
                    id='reactive-category',
                    options=[{'label': str(category).title(), 'value': reactive_categories[category]} for category in
                             reactive_categories.keys()],
                    value=list(reactive_categories.values())[0],
                    multi=False,
                    style={'width': '100%'}
                ),
                dcc.Graph(
                    id='reactive-plot',
                    style={'width': '100%'}
                ),
            ],
            style={'width': '50%', 'float': 'left', 'marginTop': '5px'}
        ),
        html.Div(
            children=[
                dcc.Graph(
                    id='library-strategy-plot',
                    style={'width': '100%', 'marginTop': 20}
                ),
            ],
            style={'width': '50%', 'float': 'left', 'marginTop': '5px'}
        ),
    ],
    style={'font-family': 'Arial', 'margin': 'auto', 'padding': '10px'}
)


@app.callback(
    Output('dto-pie-plot', 'figure'),
    [Input('dropdown-category', 'value')]
)
def update_pie_plot(category):
    return custom_plots(category, 'dto_donut')


@app.callback(
    Output('library-strategy-plot', 'figure'),
    [Input('dropdown-category', 'value')]
)


def update_library_strategy_plot(category):
    return custom_plots(category, 'library_strategy')


@app.callback(
    Output('model-type-plot', 'figure'),
    [Input('dropdown-category', 'value')]
)
def update_model_type_plot(category):
    return model_type_pie(category)


@app.callback(
    Output('venn-plot', 'figure'),
    Output('table-container', 'style'),
    Output('table', 'data'),
    [Input('dropdown-category', 'value')]
)
def update_selected_plot(selected_category):
    return custom_plots(selected_category, 'dt_venn')


@app.callback(
    Output('reactive-plot', 'figure'),
    [Input('dropdown-category', 'value'), Input('reactive-category', 'value')]
)
def update_reactive_plot(release, category):
    return reactive_bar_plot(release, category)


@app.callback(
    Output('overview-bar-chart', 'figure'),
    Input('dropdown-category', 'value')

)
def update_bar_chart(value):
    return bar_chart()
