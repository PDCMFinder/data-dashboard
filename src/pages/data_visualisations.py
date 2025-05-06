from dash import html, dcc, Dash
from dash.dependencies import Input, Output
from src.components.pages.data_visualisation import generate_expression_boxplot
from src.components.boxplot.elements import expression_boxplot_component
from src.components.ideogram.elements import mutation_ideogram_component
from src.components.pages.data_visualisation import generate_mutation_ideogram
from src.components.navbar.navbar import navbar
from src.assets.resources import gene_list, visualisation_cancer_system

def markdowns(text):
    return dcc.Markdown(f'#### {text}: ', style={'display': 'block', 'padding-left': '1%', 'margin': '0',
                            'fontSize': '18px', 'fontWeight': 'bold', 'color': '#013e48', 'width': 'max-xontent', 'white-space': 'nowrap'}),

padding = "0.1%"
margin_left = '1%'
margin_bottom = "0.1%"
app = Dash(__name__)

app.layout = html.Div(children=[
    navbar(),
    html.Div(children=[
        html.Div(children=[
            markdowns("Cancer System")[0],
            dcc.Dropdown(
                id='cancer-system-dropdown-category',
                options=[{'label': category, 'value': category} for category in
                         visualisation_cancer_system],
                value=visualisation_cancer_system,
                multi=True,
                style={'width': '90%', 'display': 'inline-block', 'marginLeft': margin_left, 'fontSize': '16px'}
            ),
        ], style={'width': '40%', 'display': 'flex', 'alignItems': 'center'}
        ),
        html.Div(children=[
            markdowns('Gene Symbol')[0],
            dcc.Dropdown(
                id='gene-symbol-dropdown-category',
                options=[{'label': category, 'value': category} for category in
                         gene_list],
                value=gene_list[0],
                multi=False,

                style={'width': '90%', 'display': 'inline-block', 'fontSize': '16px', 'marginLeft': margin_left}
            ),
        ], style={'width': '30%', 'display': 'flex', 'alignItems': 'center'}),
        html.Div(children=[
            markdowns('Model type')[0],
            dcc.RadioItems(['All', 'PDX', 'cell Line', 'organoid'], 'All', inline=True, id='model-type',
                   style={'width': '75%', 'display': 'inline-block', 'marginLeft': margin_left,
                                                  'fontSize': '16px'}),
            ], style={'width': '30%', 'display': 'flex', 'alignItems': 'center'}),
    ], style={'width': '100%', 'display': 'flex', 'padding': '1px 0', 'backgroundColor': '#f2f2f2',
              'border': '1px solid #ddd', 'borderRadius': '8px', 'margin-bottom': margin_bottom}
    ),
    html.Div(children=[expression_boxplot_component()]),
    html.Div(children=[
        html.Div(children=[
            markdowns("Cancer System")[0],
            dcc.Dropdown(
                id='cancer-system-dropdown-single-category',
                options=[{'label': category, 'value': category} for category in
                         visualisation_cancer_system],
                value=visualisation_cancer_system[0],
                style={'width': '90%', 'display': 'inline-block', 'marginLeft': margin_left, 'fontSize': '16px'}
            ),
        ], style={'width': '50%', 'display': 'flex', 'alignItems': 'center'}
        ),
    ], style={'width': '100%', 'display': 'flex', 'padding': '1px 0', 'backgroundColor': '#f2f2f2',
              'border': '1px solid #ddd', 'borderRadius': '8px', 'margin-bottom': margin_bottom}),
    mutation_ideogram_component()
    ],
    style={'font-family': 'Merriweather', 'padding': padding}
)


def register_callbacks(app):
    @app.callback(
        Output('expression-boxplot-cs-gl-mt', 'figure'),
        [Input('cancer-system-dropdown-category', 'value'),
         Input('gene-symbol-dropdown-category', 'value'),
         Input('model-type', 'value')]
    )
    def plot_expression_boxplot(cancer_system, gene_symbol, model_type):
        return generate_expression_boxplot(cancer_system, gene_symbol, model_type)

    @app.callback(
        Output('mutation-ideogram', 'annotations'),
        [Input('cancer-system-dropdown-single-category', 'value'),])
    def plot_mutation_ideogram(cancer_system):
        return generate_mutation_ideogram(cancer_system)


