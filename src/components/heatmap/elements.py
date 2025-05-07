from dash import html, dcc
from src.assets.resources import component_style_5
from src.assets.resources import gene_list, visualisation_cancer_system

def markdowns(text):
    return dcc.Markdown(f'#### {text}: ', style={'display': 'block', 'padding-left': '1%', 'margin': '0',
                            'fontSize': '18px', 'fontWeight': 'bold', 'color': '#013e48', 'width': 'max-xontent', 'white-space': 'nowrap'}),

padding = "0.1%"
margin_left = '1%'
margin_bottom = "0.1%"



def expression_heatmap_component():
    return html.Div(children=[
            dcc.Markdown('### Expression data - Heatmap:', style={'display': 'inline-block'}),

            html.Div(children=[
                html.Div(children=[
                    markdowns("Cancer System")[0],
                    dcc.Dropdown(
                        id='cancer-system-dropdown-category-1',
                        options=[{'label': category, 'value': category} for category in
                                 visualisation_cancer_system],
                        value=visualisation_cancer_system[0],
                        multi=False,
                        style={'width': '90%', 'display': 'inline-block', 'marginLeft': margin_left, 'fontSize': '16px'}
                    ),
                ], style={'width': '40%', 'display': 'flex', 'alignItems': 'center'}
                ),
                html.Div(children=[
                    markdowns('Gene Symbol')[0],
                    dcc.Dropdown(
                        id='gene-symbol-dropdown-category-1',
                        options=[{'label': category, 'value': category} for category in
                                 gene_list],
                        value=gene_list,
                        multi=True,

                        style={'width': '90%', 'display': 'inline-block', 'fontSize': '16px', 'marginLeft': margin_left}
                    ),
                ], style={'width': '30%', 'display': 'flex', 'alignItems': 'center'}),
                html.Div(children=[
                    markdowns('Model type')[0],
                    dcc.RadioItems(['All', 'PDX', 'cell Line', 'organoid'], 'All', inline=True, id='model-type-1',
                                   style={'width': '75%', 'display': 'inline-block', 'marginLeft': margin_left,
                                          'fontSize': '16px'}),
                ], style={'width': '30%', 'display': 'flex', 'alignItems': 'center'}),
            ], style={'width': '100%', 'display': 'flex', 'padding': '1px 0', 'backgroundColor': '#f2f2f2',
                      'border': '1px solid #ddd', 'borderRadius': '8px', 'margin-bottom': margin_bottom}
            ),

            dcc.Graph(id='expression-heatmap-cs-gl-mt', style={'width': '100%'}),
        ], style=component_style_5)