from dash import dcc, html

def navbar():
    return html.Div(
        children=[
            html.H1(
                "Data Overview Dashboard",
                style={
                    'textAlign': 'left',
                    'backgroundColor': '#013e48',
                    'color': '#013e48',
                    'padding': '2.5% 20px',  # Add some padding for spacing
                    'margin': 0,
                    'fontFamily': 'Arial, sans-serif',
                    'fontSize': '24px',
                    'background-image': 'url("/assets/cover.png")',  # Set the background image
                    'background-size': '100% 375%',  # Cover the entire header
                    'background-repeat': 'no-repeat',
                    'background-position': 'right',
                    'background-position-y': '53%'
                }
            ),
            html.Div(
                children=[
                    dcc.Link(
                        'Home',
                        href='/',
                        className='nav-link',
                        style={"color": "white", "padding": "10px 20px", "textDecoration": "none"}
                    ),
                    dcc.Link(
                        'Data Releases',
                        href='/data-release',
                        className='nav-link',
                        style={"color": "white", "padding": "10px 20px", "textDecoration": "none"}
                    ),
                    dcc.Link(
                        'Metadata scores',
                        href='/metadata-scores',
                        className='nav-link',
                        style={"color": "white", "padding": "10px 20px", "textDecoration": "none"}
                    ),
                    dcc.Link(
                        'Data Visualisation',
                        href='/data-visualisations',
                        className='nav-link',
                        style={"color": "white", "padding": "10px 20px", "textDecoration": "none"}
                    ),
                ],
                className='navbar',
                style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'flex-start',  # Align links to the left
                    'padding': '1px 20px',
                    'backgroundColor': '#013e48',
                    'gap': '15px'  # Space between links
                }
            )
        ],
        style={
            'backgroundColor': '#013e48',
            'color': '#ffffff',
            'margin-bottom': '0.5%',
            'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'  # Add subtle shadow for depth
        }
    )
