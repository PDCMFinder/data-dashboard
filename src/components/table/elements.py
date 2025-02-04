import pandas as pd
from dash import html, dcc, dash_table
from src.assets.resources import component_style_5

df = pd.DataFrame(columns=["model_id", "provider", "model_type", "PDCM_DR_v1.0", "PDCM_DR_v2.0", "PDCM_DR_v2.1", "PDCM_DR_v3.0", "PDCM_DR_v3.1", "PDCM_DR_v4.0", "PDCM_DR_v5.0", "PDCM_DR_v5.1", "PDCM_DR_v5.2", "PDCM_DR_v5.3", "PDCM_DR_v6.0", "PDCM_DR_v6.1", "PDCM_DR_v6.2", "PDCM_DR_v6.3", "PDCM_DR_v6.4", "PDCM_DR_v6.5", "PDCM_DR_v6.6", "PDCM_DR_v6.7"])

def score_table_component():
    return html.Div(children=[
        dash_table.DataTable(
        id='data-table-ms',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        page_size=15,
        filter_action='native',  # Allow column filtering
        sort_action='native',  # Allow sorting by columns
        row_selectable='multi',  # Allow row selection
        selected_rows=[],
        style_table={'overflowX': 'auto'},  # Handle overflow of columns
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'rgb(210, 210, 210)',
            'color': 'black',
            'fontWeight': 'bold'
        },
        export_format='xlsx',
        export_headers='display',
    ),
    dcc.Graph(id='ms-line-plot')
    ], style=component_style_5
    )