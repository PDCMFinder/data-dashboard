from dash import html, dcc
from src.assets.resources import component_style_5
from dash_bio import Ideogram

def mutation_ideogram_component():
    return html.Div(children=[
            dcc.Markdown('### Mutation data - Ideogram:', style={'display': 'inline-block'}),
            Ideogram(
                id='mutation-ideogram',
                annotationsLayout='overlay'
            ),
        ], style=component_style_5)