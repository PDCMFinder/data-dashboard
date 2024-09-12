from dash import html, dcc
from src.components.resources import component_style_1, component_style_2

def ui_model_type_component():
    return html.Div(children=[
            dcc.Markdown('### Model type overview:', style={'display': 'inline-block'}),
            dcc.Graph(id='model-type-plot', style={'width': '100%'}),
            html.Div([html.Button("Export to CSV", id="btn_csv_mto"), dcc.Download(id="download-dataframe-csv-mto")]),
        ], style=component_style_1)

def ui_data_type_overview_component():
    return html.Div(children=[
        dcc.Markdown('### Data type overview:', style={'display': 'inline-block'}),
        dcc.Graph(id='dto-pie-plot', style={'width': '100%'}),
        html.Div([html.Button("Export to CSV", id="btn_csv_dto"), dcc.Download(id="download-dataframe-csv-dto")]),
    ], style=component_style_1)

def ui_molecular_data_tech_overview_component():
    return html.Div(children=[
            dcc.Markdown('### Molecular data by Technology used:', style={'display': 'inline-block'}),
            dcc.Graph(id='library-strategy-plot', style={'width': '100%'}),
            html.Div([html.Button("Export to CSV", id="btn_csv_lsp"), dcc.Download(id="download-dataframe-csv-lsp")]),
    ], style=component_style_2
    )