from dash import html, dcc, Dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from src.assets.resources import labels, engine
from urllib.parse import urlparse, parse_qs
from src.components.navbar.navbar import navbar
from src.components.pie.elements import ui_model_type_component, ui_data_type_overview_component, ui_molecular_data_tech_overview_component
from src.components.bar.elements import ui_country_plots_component, ui_molecular_data_type_by_model_type_component, ui_model_counts_component
from src.components.overlap.elements import ui_overlap_diagram_element
from src.components.pages.release import generate_overlap_diagram, model_type_pie, reactive_bar_plot, generate_country_plot, molecular_model_type_plot, dto_donut, library_strategy, dt_venn, venn4_plots



padding = "0.1%"
margin_left = '0.1%'
margin_bottom = "0.1%"
app = Dash(__name__)
app.layout = html.Div(children=[
    navbar(),
    html.Div(children=[
        dcc.Markdown('### Select Data release: ', style={'display': 'inline-block', 'padding-left': '1%', 'margin': '0',
                        'fontSize': '18px', 'fontWeight': 'bold', 'color': '#013e48'}),
        dcc.Dropdown(
            id='dropdown-category',
            options=[{'label': str(labels[category]).title(), 'value': category} for category in
                     labels.keys()],
            value=list(labels.keys())[0],
            multi=False,
            style={'width': '50%', 'display': 'inline-block', 'marginLeft': margin_left, 'fontSize': '16px'}
        )], style={'width': '100%', 'display': 'inline-block', 'display': 'flex', 'alignItems': 'center', 'gap': '2px',
                   'padding': '1px 0', 'backgroundColor': '#f2f2f2', 'border': '1px solid #ddd', 'borderRadius': '8px',
                   'margin-bottom': margin_bottom}),
    ui_model_type_component(),
    ui_data_type_overview_component(),

    html.Div(children=[
            dcc.Markdown('### Model data overlap:', style={'display': 'inline-block'}),
            dcc.RadioItems(['Total', 'PDX', 'Cell Line', 'Organoid'], 'Total', inline=True, id='venn-type'),
            html.Div(dcc.Graph(id='venn-plot'), id='venn-plot-container'),
            dcc.Store(id='div-width-venn'),
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
        style={'border': '0.5px solid #000', 'background-color': '#f4f4f4', 'padding': '0.5%',
               'border-radius': '10px', 'width': '33.3%', 'float': 'right', 'margin-bottom': margin_bottom, 'margin-left': '0.1%'}
    ),
    ui_model_counts_component(),
    ui_molecular_data_tech_overview_component(),
    ui_country_plots_component(),
    ui_molecular_data_type_by_model_type_component(),
    ui_overlap_diagram_element(),
    ],
    style={'font-family': 'Merriweather', 'padding': padding}
)

def register_callbacks(app):
    @app.callback(
            Output('dropdown-category', 'value'),
            [Input('url', 'href')]
    )
    def set_dropdown_value(href):
        # Parse the URL to get query parameters
        if href:
            parsed_url = urlparse(href)
            query_params = parse_qs(parsed_url.query)
            # Extract filter value from query params
            filter_value = query_params.get('dropdown-category', [None])[0]
            if filter_value in labels.keys():
                return filter_value
        return list(labels.keys())[0]


    @app.callback(
        Output('dto-pie-plot', 'figure'),
        [Input('dropdown-category', 'value')]
    )
    def update_pie_plot(category):
        return dto_donut(engine, category)


    @app.callback(
        Output('library-strategy-plot', 'figure'),
        [Input('dropdown-category', 'value')]
    )
    def update_library_strategy_plot(category):
        return library_strategy(engine, category, )


    @app.callback(
        Output('model-type-plot', 'figure'),
        [Input('dropdown-category', 'value')]
    )
    def update_model_type_plot(category):
        return model_type_pie(engine, category, 'plot')

    app.clientside_callback(
        """
        function(_, trigger_id) {
            const element = document.getElementById("graph-container");
            if (element) {
                return element.offsetWidth;
            }
            return 0;
        }
        """,
        Output("div-width", "data"),
        Input("overlap-diagram", "id"),
    )

    app.clientside_callback(
        """
        function(_, trigger_id) {
            const element = document.getElementById("venn-plot-container");
            if (element) {
                return element.offsetWidth;
            }
            return 0;
        }
        """,
        Output("div-width-venn", "data"),
        Input("venn-plot", "id"),
    )

    @app.callback(
        Output('overlap-diagram', 'figure'),
        [Input('dropdown-category', 'value'), Input("div-width", "data")]
    )
    def update_overlap_diagram(selected_category, width):
        return generate_overlap_diagram(engine, selected_category, width)

    @app.callback(
        Output('venn-plot', 'figure'),
        [Input('dropdown-category', 'value'), Input('venn-type', 'value'), Input("div-width-venn", "data")]
    )
    def update_selected_plot(selected_category, venn_type, width):
        return dt_venn(engine, selected_category, f'dt_venn_{venn_type}', width)

    @app.callback(
        Output('venn-plot-venn4', 'figure'),
        [Input('dropdown-category', 'value')]
    )
    def update_selected_plot(selected_category):
        return venn4_plots(engine, selected_category, 'immunemarker')

    @app.callback(
        Output('venn-plot-venn4-bio', 'figure'),
        [Input('dropdown-category', 'value')]
    )
    def update_selected_plot(selected_category):
        return venn4_plots(engine, selected_category, 'biomarker')

    @app.callback(
        Output('reactive-plot', 'figure'),
        [Input('dropdown-category', 'value'), Input('reactive-category', 'value'),
         Input('reactive-groupby-category', 'value')]
    )
    def update_reactive_plot(release, category, group_cat):
        return reactive_bar_plot(engine, release, category, group_cat, 'plot')

    @app.callback(
        Output('country-plot', 'figure'),
        Output('country-table', 'data'),
        [Input('dropdown-category', 'value')]
    )
    def country_plot(selected_category):
        return generate_country_plot(engine, selected_category, 'plot')


    @app.callback(
        Output('mol-model-type-plot', 'figure'),
        [Input('dropdown-category', 'value')]
    )
    def molecular_model_type(selected_category):
        return molecular_model_type_plot(engine, selected_category, 'plot')


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
            return dt_venn(engine, release, 'dt_venn','table')

    @app.callback(
        Output("download-dataframe-csv-mto", "data"),
        [Input('dropdown-category', 'value'), Input("btn_csv_mto", "n_clicks")],
        prevent_initial_call=True,
    )
    def func(release, n_clicks):
        if not n_clicks:
            raise PreventUpdate
        else:
            return dcc.send_data_frame(model_type_pie(engine ,release, 'table').to_csv, f'{release}_mto_table.csv', index=False)


    @app.callback(
        Output("download-dataframe-csv-dto", "data"),
        [Input('dropdown-category', 'value'), Input("btn_csv_dto", "n_clicks")],
        prevent_initial_call=True,
    )
    def func(release, n_clicks):
        if not n_clicks:
            raise PreventUpdate
        else:
            return dcc.send_data_frame(dto_donut(engine, release, 'table').to_csv, f'{release}_dto_table.csv', index=False)


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
            return dcc.send_data_frame(reactive_bar_plot(engine, release, category, group_cat, 'table').to_csv, f'{release}_model_counts_table.csv', index=False)


    @app.callback(
        Output("download-dataframe-csv-country", "data"),
        [Input('dropdown-category', 'value'), Input("btn_csv_country", "n_clicks")],
        prevent_initial_call=True,
    )
    def func(release, n_clicks):
        if not n_clicks:
            raise PreventUpdate
        else:
            return dcc.send_data_frame(generate_country_plot(engine, release, 'table').to_csv, f'{release}_country_table.csv', index=False)

    @app.callback(
        Output("download-dataframe-csv-lsp", "data"),
        [Input('dropdown-category', 'value'), Input("btn_csv_lsp", "n_clicks")],
        prevent_initial_call=True,
    )
    def func(release, n_clicks):
        if not n_clicks:
            raise PreventUpdate
        else:
            return dcc.send_data_frame(library_strategy(engine, release, 'table').to_csv, f'{release}_library_table.csv', index=False)

    @app.callback(
        Output("download-dataframe-csv-mmtp", "data"),
        [Input('dropdown-category', 'value'), Input("btn_csv_mmtp", "n_clicks")],
        prevent_initial_call=True,
    )
    def func(release, n_clicks):
        if not n_clicks:
            raise PreventUpdate
        else:
            return dcc.send_data_frame(molecular_model_type_plot(engine, release, 'table').to_csv, f'{release}_molecular_model_type_table.csv', index=False)

