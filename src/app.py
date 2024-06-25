import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from src.util import *
from src.resources import labels, reactive_categories
from io import BytesIO
from base64 import b64decode


backend = get_release_data("")
padding = "0.5%"
margin_left = '0.45%'
margin_bottom = "0.5%"
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1("CancerModels.Org - Data Overview Dashboard",
            style={'textAlign': 'left', 'backgroundColor': '#013e48', 'color': '#ffffff',
                   'padding': '0.2%', 'padding-top': '2%'}),
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
                        },
                    export_format='xlsx',
                    export_headers='display',
                    ),
                ], style={'width': '50%', 'float': 'right'}),
                ]),
    ], style={'height': '10%', 'width': '100%'}
    ),
    html.Div(children=[
        dcc.Markdown('### Select Data release: ', style={'display': 'inline-block'}),
        dcc.Dropdown(
            id='dropdown-category',
            options=[{'label': str(labels[category]).title(), 'value': category} for category in
                     labels.keys()],
            value=list(labels.keys())[0],
            multi=False,
            style={'width': '50%', 'display': 'inline-block'}
        )], style={'width': '100%', 'display': 'inline-block'}),
    html.Div(children=[
        dcc.Markdown('### Model type overview:', style={'display': 'inline-block'}),
        dcc.Graph(
            id='model-type-plot',
            style={'width': '100%'}
        ),
        html.Div([
                html.Button("Export to CSV", id="btn_csv_mto"),
                dcc.Download(id="download-dataframe-csv-mto")
            ]),
        ],
        style={'border': '0.5px solid #000', 'background-color': '#f4f4f4', 'padding': padding,
               'border-radius': '10px', 'width': '31.5%', 'float': 'left', 'margin-bottom': margin_bottom}
    ),
    html.Div(children=[
            dcc.Markdown('### Data type overview:', style={'display': 'inline-block'}),
            dcc.Graph(
                id='dto-pie-plot',
                style={'width': '100%'}
            ),
            html.Div([
                html.Button("Export to CSV", id="btn_csv_dto"),
                dcc.Download(id="download-dataframe-csv-dto")
            ]),
        ],
        style={'border': '0.5px solid #000', 'background-color': '#f4f4f4', 'padding': padding,
               'border-radius': '10px', 'width': '31.5%', 'float': 'left', 'margin-left': margin_left, 'margin-bottom': margin_bottom}
    ),
    html.Div(children=[
            dcc.Markdown('### Model data overlap:', style={'display': 'inline-block'}),
            dcc.RadioItems(['Total', 'PDX', 'Cell Line', 'Organoid'], 'Total', inline=True, id='venn-type'),
            html.Div(dcc.Graph(id='venn-plot'),),
            html.Div(dcc.Graph(
                id='venn-plot-venn4',
                figure={
                'data': [],
                'layout': {
                    'images': [{
                        'source': None,
                        'xref': 'paper',
                        'yref': 'paper',
                        'x': 0.5,
                        'y': 0.5,
                        'sizex': 1,
                        'sizey': 1,
                        'xanchor': 'center',
                        'yanchor': 'middle'
                    }],
                    'xaxis': {'visible': False},
                    'yaxis': {'visible': False}
                }
        }
                ),
            ),
            html.Div(dcc.Graph(
                    id='venn-plot-venn4-bio',
                    figure={
                    'data': [],
                    'layout': {
                        'images': [{
                            'source': None,
                            'xref': 'paper',
                            'yref': 'paper',
                            'x': 0.5,
                            'y': 0.5,
                            'sizex': 1,
                            'sizey': 1,
                            'xanchor': 'center',
                            'yanchor': 'middle'
                        }],
                        'xaxis': {'visible': False},
                        'yaxis': {'visible': False}
                    }
            }
                ),
            ),
            html.Div([
                html.Button("Export to XLS", id="btn_csv"),
                dcc.Download(id="download-dataframe-csv")
            ],
                id='table-container',
            ),
        ],
        style={'border': '0.5px solid #000', 'background-color': '#f4f4f4', 'padding': padding,
               'border-radius': '10px', 'width': '33%', 'float': 'right', 'margin-bottom': margin_bottom}
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
                        style={'width': '40%', 'display': 'inline-block'}
                    ),
                    dcc.Markdown('Group by:', style={'display': 'inline-block'}),
                    dcc.Dropdown(
                        id='reactive-groupby-category',
                        options=[{'label': str(category).title(), 'value': reactive_categories[category]} for category in
                                 reactive_categories.keys()],
                        value=None,
                        multi=False,
                        style={'width': '40%', 'display': 'inline-block'}
                    ),
                    html.Div([
                        html.Button("Export to CSV", id="btn_csv_model_counts"),
                        dcc.Download(id="download-dataframe-csv-model_counts")
                    ]),
                ],
                style={'width': '100%'}
            ),
            dcc.Graph(
                id='reactive-plot',
                style={'width': '100%'}
            ),
        ],
        style={'border': '0.5px solid #000', 'background-color': '#f4f4f4', 'padding': padding,
               'border-radius': '10px', 'width': '64.5%', 'float': 'left', 'margin-bottom': margin_bottom}
    ),
    html.Div(children=[
            dcc.Markdown('### Molecular data by Technology used:', style={'display': 'inline-block'}),
            dcc.Graph(
                id='library-strategy-plot',
                style={'width': '100%'}
            ),
            html.Div([
                html.Button("Export to CSV", id="btn_csv_lsp"),
                dcc.Download(id="download-dataframe-csv-lsp")
            ]),
    ],
        style={'border': '0.5px solid #000', 'background-color': '#f4f4f4', 'padding': padding,
               'border-radius': '10px', 'width': '64.5%', 'float': 'left', 'margin-bottom': margin_bottom}
    ),
    html.Div(children=[
            dcc.Markdown('### Provider country plot:', style={'display': 'inline-block'}),
            html.Div([
                html.Button("Export to CSV", id="btn_csv_country"),
                dcc.Download(id="download-dataframe-csv-country")
            ]),

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
                export_format='csv',
                export_headers='display',
            ),
            ],
            style={'border': '0.5px solid #000', 'background-color': '#f4f4f4', 'padding': padding,
                        'border-radius': '10px', 'width': '33%', 'float': 'right', 'margin-bottom': margin_bottom}
            ),
    html.Div(children=[
            dcc.Markdown('### Molecular data by model type:', style={'display': 'inline-block'}),
            dcc.Graph(
                id='mol-model-type-plot',
                style={'width': '100%'}
            ),
            html.Div([
                html.Button("Export to CSV", id="btn_csv_mmtp"),
                dcc.Download(id="download-dataframe-csv-mmtp")
            ]),
        ],
        style={'border': '0.5px solid #000', 'background-color': '#f4f4f4', 'padding': padding,
               'border-radius': '10px', 'width': '64.5%', 'float': 'left', 'margin-bottom': margin_bottom}
    ),
    ],
    style={'font-family': 'Merriweather', 'padding': padding}
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
    return model_type_pie(category, 'plot')


@app.callback(
    Output('venn-plot', 'figure'),
    [Input('dropdown-category', 'value'), Input('venn-type', 'value'),]
)
def update_selected_plot(selected_category, venn_type):
    return custom_plots(selected_category, f'dt_venn_{venn_type}')

@app.callback(
    Output('venn-plot-venn4', 'figure'),
    [Input('dropdown-category', 'value')]
)
def update_selected_plot(selected_category):
    return custom_plots(selected_category, 'dt_v4venn')

@app.callback(
    Output('venn-plot-venn4-bio', 'figure'),
    [Input('dropdown-category', 'value')]
)
def update_selected_plot(selected_category):
    return custom_plots(selected_category, 'dt_v4venn', 'biomarker')

@app.callback(
    Output('reactive-plot', 'figure'),
    [Input('dropdown-category', 'value'), Input('reactive-category', 'value'),
     Input('reactive-groupby-category', 'value')]
)
def update_reactive_plot(release, category, group_cat):
    return reactive_bar_plot(release, category, group_cat, 'plot')


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
    return generate_country_plot(selected_category, 'plot')


@app.callback(
    Output('mol-model-type-plot', 'figure'),
    [Input('dropdown-category', 'value')]
)
def molecular_model_type(selected_category):
    return molecular_model_type_plot(selected_category, 'plot')


## Exports
@app.callback(
    Output("download-dataframe-csv", "data"),
    [Input('dropdown-category', 'value'), Input("btn_csv", "n_clicks")],
    prevent_initial_call=True,
)
def func(release, n_clicks):
    if not n_clicks:
        raise PreventUpdate
    else:
        return custom_plots(release, 'dt_venn','table')

@app.callback(
    Output("download-dataframe-csv-mto", "data"),
    [Input('dropdown-category', 'value'), Input("btn_csv_mto", "n_clicks")],
    prevent_initial_call=True,
)
def func(release, n_clicks):
    if not n_clicks:
        raise PreventUpdate
    else:
        return dcc.send_data_frame(model_type_pie(release, 'table').to_csv, f'{release}_mto_table.csv', index=False)


@app.callback(
    Output("download-dataframe-csv-dto", "data"),
    [Input('dropdown-category', 'value'), Input("btn_csv_dto", "n_clicks")],
    prevent_initial_call=True,
)
def func(release, n_clicks):
    if not n_clicks:
        raise PreventUpdate
    else:
        return dcc.send_data_frame(custom_plots(release, 'dto_donut', 'table').to_csv, f'{release}_dto_table.csv', index=False)


@app.callback(
    Output("download-dataframe-csv-model_counts", "data"),
    [Input('dropdown-category', 'value'),
     Input('reactive-category', 'value'),
     Input('reactive-groupby-category', 'value'),
     Input("btn_csv_model_counts", "n_clicks")],
    prevent_initial_call=True,
)
def func(release, category, group_cat, n_clicks):
    if not n_clicks:
        raise PreventUpdate
    else:
        return dcc.send_data_frame(reactive_bar_plot(release, category, group_cat, 'table').to_csv, f'{release}_model_counts_table.csv', index=False)


@app.callback(
    Output("download-dataframe-csv-country", "data"),
    [Input('dropdown-category', 'value'), Input("btn_csv_country", "n_clicks")],
    prevent_initial_call=True,
)
def func(release, n_clicks):
    if not n_clicks:
        raise PreventUpdate
    else:
        return dcc.send_data_frame(generate_country_plot(release, 'table').to_csv, f'{release}_country_table.csv', index=False)

@app.callback(
    Output("download-dataframe-csv-lsp", "data"),
    [Input('dropdown-category', 'value'), Input("btn_csv_lsp", "n_clicks")],
    prevent_initial_call=True,
)
def func(release, n_clicks):
    if not n_clicks:
        raise PreventUpdate
    else:
        return dcc.send_data_frame(custom_plots(release, 'library_strategy', 'table').to_csv, f'{release}_library_table.csv', index=False)

@app.callback(
    Output("download-dataframe-csv-mmtp", "data"),
    [Input('dropdown-category', 'value'), Input("btn_csv_mmtp", "n_clicks")],
    prevent_initial_call=True,
)
def func(release, n_clicks):
    if not n_clicks:
        raise PreventUpdate
    else:
        return dcc.send_data_frame(molecular_model_type_plot(release, 'table').to_csv, f'{release}_molecular_model_type_table.csv', index=False)

