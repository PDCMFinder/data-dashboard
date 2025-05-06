from dash import html, dcc
from src.assets.resources import component_style_5

def expression_boxplot_component():
    return html.Div(children=[
            dcc.Markdown('### Expression data - Boxplot:', style={'display': 'inline-block'}),
            dcc.Graph(id='expression-boxplot-cs-gl-mt', style={'width': '100%'}),
        ], style=component_style_5)