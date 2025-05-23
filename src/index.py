# index.py
from dash import dcc, html
from dash.dependencies import Input, Output
from src.pages.home import app as home_page_layout, register_callbacks as home_callbacks_layout
from src.pages.release import app as release_page_layout, register_callbacks as release_callbacks_layout
from src.pages.metadata_scores import app as ms_page_layout, register_callbacks as ms_callbacks_layout
from src.pages.data_visualisations import app as ds_page_layout, register_callbacks as data_visualisations_callbacks_layout

def register_callbacks(app):
    home_callbacks_layout(app)
    release_callbacks_layout(app)
    ms_callbacks_layout(app)
    data_visualisations_callbacks_layout(app)
    @app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        if pathname == '/data-release':
            return release_page_layout.layout
        elif pathname == '/metadata-scores':
            return ms_page_layout.layout
        elif pathname == '/data-visualisations':
            return ds_page_layout.layout
        else:
            return home_page_layout.layout