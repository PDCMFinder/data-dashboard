import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
from src.util import *
from src.resources import labels, input_file, reactive_categories

app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1("CancerModels.Org - Data Overview Dashboard",
            style={'textAlign': 'left', 'marginBottom': 20, 'backgroundColor': '#013e48', 'color': '#ffffff',
                   'padding': '0.1%', 'padding-top': '2%'}),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[dcc.Graph(id='overview-bar-chart',)], style={'width': '50%', 'float': 'left'}),
            html.Div(children=[
                dcc.Markdown('### Summary Stats:', style={'display': 'inline-block'}),
                dash_table.DataTable(
                    id='summary-stat-table',
                    columns=[
                        {'name': col, 'id': col} for col in list(summary.columns)
                    ],
                    data=summary.to_dict('records'),
                    style_table={'overflow': 'auto'},
                    style_cell={'textAlign': 'left'},
                    style_header={
                            'backgroundColor': 'rgb(210, 210, 210)',
                            'color': 'black',
                            'fontWeight': 'bold'
                        }
                    ),
                ], style={'width': '50%', 'float': 'right'}),
                ]),
    ], style={'height': '10%', 'width': '100%', 'margin': 'auto', 'marginTop': '-10'}
    ),
    html.Div(children=[
        dcc.Markdown('### Select Data release: ', style={'display': 'inline-block'}),
        dcc.Dropdown(
            id='dropdown-category',
            options=[{'label': str(labels[category]).title(), 'value': category} for category in
                     input_file.keys()],
            value=list(input_file.keys())[0],
            multi=False,
            style={'width': '50%', 'display': 'inline-block'}
        )], style={'width': '100%', 'display': 'inline-block'}),
    html.Div(children=[
        dcc.Markdown('### Model type overview:', style={'display': 'inline-block'}),
        dcc.Graph(
            id='model-type-plot',
            style={'width': '100%', 'marginTop': 20}
        ),
        ],
        style={'border': '0.5px solid #000', 'background-color': '#f4f4f4', 'padding': '10px',
               'border-radius': '10px', 'width': '32%', 'float': 'left', 'marginTop': '5px', 'marginLeft': '0px'}
    ),
    html.Div(children=[
            dcc.Markdown('### Data type overview:', style={'display': 'inline-block'}),
            dcc.Graph(
                id='dto-pie-plot',
                style={'width': '100%', 'marginTop': 20}
            ),
        ],
        style={'border': '0.5px solid #000', 'background-color': '#f4f4f4', 'padding': '10px',
               'border-radius': '10px', 'width': '32%', 'float': 'left', 'marginTop': '5px', 'marginLeft': '5px'}
    ),
    html.Div(children=[
            dcc.Markdown('### Model data overlap:', style={'display': 'inline-block'}),
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
                style={'marginTop': '10px'},
                id='table-container',
            ),
        ],
        style={'border': '0.5px solid #000', 'background-color': '#f4f4f4', 'padding': '10px',
               'border-radius': '10px', 'width': '31.5%', 'float': 'right', 'marginTop': '5px', 'marginLeft': '5px'}
    ),
    html.Div(children=[
            html.Div(
                children=[
                    dcc.Markdown('### Model counts plot:'),
                    dcc.Markdown('Attribute:', style={'display': 'inline-block'}),
                    dcc.Dropdown(
                        id='reactive-category',
                        options=[{'label': str(category).title(), 'value': reactive_categories[category]} for category in
                                 reactive_categories.keys()],
                        value=list(reactive_categories.values())[0],
                        multi=False,
                        style={'width': '40%', 'display': 'inline-block', 'margin-left': '5px'}
                    ),
                    dcc.Markdown('Group by:', style={'display': 'inline-block'}),
                    dcc.Dropdown(
                        id='reactive-groupby-category',
                        options=[{'label': str(category).title(), 'value': reactive_categories[category]} for category in
                                 reactive_categories.keys()],
                        value=None,
                        multi=False,
                        style={'width': '40%', 'display': 'inline-block', 'margin-left': '5px'}
                    ),
                ],
                style={'width': '100%'}
            ),
            dcc.Graph(
                id='reactive-plot',
                style={'width': '100%'}
            ),
        ],
        style={'border': '0.5px solid #000', 'background-color': '#f4f4f4', 'padding': '10px',
               'border-radius': '10px', 'width': '64.5%', 'float': 'left', 'marginTop': '5px'}
    ),
    html.Div(children=[
        dcc.Markdown('### Provider country plot:', style={'display': 'inline-block'}),
        dcc.Graph(
            id='country-plot',
            style={'width': '100%'}
        ),
        dash_table.DataTable(
            id='country-table',
            columns=[
                {'name': col, 'id': col} for col in list(country.columns)
            ],
            data=country.to_dict('records'),
            style_table={'overflow': 'auto'},
            style_cell={'textAlign': 'left'},
        ),
        ],
        style={'border': '0.5px solid #000', 'background-color': '#f4f4f4', 'padding': '10px',
                    'border-radius': '10px', 'width': '32.5%', 'float': 'right', 'marginTop': '5px',
                    'marginLeft': '5px'}
        ),
    html.Div(children=[
            dcc.Markdown('### Molecular data by Technology used:', style={'display': 'inline-block'}),
            dcc.Graph(
                id='library-strategy-plot',
                style={'width': '100%'}
            ),
        ],
        style={'border': '0.5px solid #000', 'background-color': '#f4f4f4', 'padding': '10px',
               'border-radius': '10px', 'width': '64.5%', 'float': 'left', 'marginTop': '5px', 'marginLeft': '0px'}
    ),
    html.Div(children=[
            dcc.Markdown('### Molecular data by model type:', style={'display': 'inline-block'}),
            dcc.Graph(
                id='mol-model-type-plot',
                style={'width': '100%'}
            ),
        ],
        style={'border': '0.5px solid #000', 'background-color': '#f4f4f4', 'padding': '10px',
               'border-radius': '10px', 'width': '64.5%', 'float': 'left', 'marginTop': '5px', 'marginLeft': '0px'}
    ),
    ],
    style={'font-family': 'Merriweather', 'margin': 'auto', 'padding': '10px'}
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
    [Input('dropdown-category', 'value'), Input('reactive-category', 'value'),
     Input('reactive-groupby-category', 'value')]
)
def update_reactive_plot(release, category, group_cat):
    return reactive_bar_plot(release, category, group_cat)


@app.callback(
    Output('overview-bar-chart', 'figure'),
    Input('dropdown-category', 'value')

)
def update_bar_chart(value):
    return bar_chart()

@app.callback(
    Output('summary-stat-table', 'data'),
    Input('dropdown-category', 'value')
)
def update_summary_stats(category):
    return generate_summary_stats()


@app.callback(
    Output('country-plot', 'figure'),
    Output('country-table', 'data'),
    [Input('dropdown-category', 'value')]
)
def country_plot(selected_category):
    return generate_country_plot(selected_category)


@app.callback(
    Output('mol-model-type-plot', 'figure'),
    [Input('dropdown-category', 'value')]
)
def molecular_model_type(selected_category):
    return molecular_model_type_plot(selected_category)
