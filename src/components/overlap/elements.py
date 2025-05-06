from dash import html, dcc
from src.assets.resources import component_style_5

margin_bottom = "0.1%"
def ui_overlap_diagram_element():
    return html.Div(children=[
            dcc.Markdown('### Model data overlap diagram:', style={'display': 'inline-block'}),
            #dcc.RadioItems(['Total', 'PDX', 'Cell Line', 'Organoid'], 'Total', inline=True, id='venn-type'),
            html.Div(dcc.Graph(id='overlap-diagram'), id='graph-container'),
            dcc.Store(id='div-width'),
        ], style=component_style_5
    )