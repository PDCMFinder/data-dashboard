from dash import html, dcc, dash_table
from src.assets.resources import reactive_categories
from src.assets.resources import component_style_2, component_style_3, component_style_4
from pandas import DataFrame

country = DataFrame(columns=['country', 'provider'])

def ui_model_counts_component():
    return html.Div(children=[
            dcc.Markdown('### Model counts plot:'),
            html.Div(
                children=[
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
                    html.Div([html.Button("Export to CSV", id="btn_csv_model_counts"),
                              dcc.Download(id="download-dataframe-csv-model_counts")]),
                ], style={'width': '100%', 'display': 'inline-block', 'display': 'flex', 'alignItems': 'center', 'gap': '2px', 'padding': '2px 0'}
            ),
            dcc.Graph(
                id='reactive-plot',
                style={'width': '100%'}
            ),
        ],
        style=component_style_2
    )

def ui_country_plots_component():
    return html.Div(children=[
            dcc.Markdown('### Provider country plot:', style={'display': 'inline-block'}),
            html.Div([html.Button("Export to CSV", id="btn_csv_country"), dcc.Download(id="download-dataframe-csv-country")]),
            dcc.Graph(id='country-plot', style={'width': '100%'}),
            dash_table.DataTable(
                id='country-table',
                columns=[{'name': col, 'id': col} for col in list(country.columns)],
                data=country.to_dict('records'),
                style_table={'overflow': 'auto'},
                style_cell={'textAlign': 'left'},
                export_format='csv',
                export_headers='display',
            ),
            ],style=component_style_3)

def ui_molecular_data_type_by_model_type_component():
    return html.Div(children=[
            dcc.Markdown('### Molecular data by model type:', style={'display': 'inline-block'}),
            dcc.Graph(id='mol-model-type-plot', style={'width': '100%'}),
            html.Div([html.Button("Export to CSV", id="btn_csv_mmtp"), dcc.Download(id="download-dataframe-csv-mmtp")]),
        ], style=component_style_2
    )

def ui_ms_bar_radio_component():
    return html.Div(children=[
        dcc.RadioItems(['PDX', 'Cell Line', 'Organoid'], 'PDX', inline=True, id='ms-category', style={'width': '50%', 'display': 'inline-block', 'marginLeft': '0.1%', 'fontSize': '16px'}),
    ], style={'width': '100%', 'display': 'inline-block', 'display': 'flex', 'alignItems': 'center', 'gap': '2px',
              'padding': '1% 0', 'backgroundColor': '#f2f2f2', 'border': '1px solid #ddd', 'borderRadius': '8px',
              'margin-bottom': '0.1%'})

def ui_ms_bar_plot_component(mt):
    return html.Div(children=[dcc.Markdown(f'### Metadata scores for {mt} models:', style={'display': 'inline-block'}),
            dcc.Graph(id=f'{mt}-model-type-plot', style={'width': '100%'}),
            html.Div([html.Button("Export", id=f"btn_csv_ms_{mt}"), dcc.Download(id=f"download-dataframe-csv-ms-{mt}")]),
        ], style=component_style_4
    )