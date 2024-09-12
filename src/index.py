# index.py
from dash import dcc, html
from dash.dependencies import Input, Output
from src.pages.home import app as home_page_layout, register_callbacks as home_callbacks_layout
from src.pages.release import app as release_page_layout, register_callbacks as release_callbacks_layout

def register_callbacks(app):
    home_callbacks_layout(app)
    release_callbacks_layout(app)
    @app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        if pathname == '/data-release':
            return release_page_layout.layout
        else:

            return home_page_layout.layout