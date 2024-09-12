from dash import dcc, html

def navbar():
    return html.Div(
        children=[
            html.H1(
                "CancerModels.Org - Data Overview Dashboard",
                style={
                    'textAlign': 'left',
                    'backgroundColor': '#013e48',
                    'color': '#ffffff',
                    'padding': '15px 20px',  # Add some padding for spacing
                    'margin': 0,
                    'fontFamily': 'Arial, sans-serif',
                    'fontSize': '24px'
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
                ],
                className='navbar',
                style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'flex-start',  # Align links to the left
                    'padding': '10px 20px',
                    'backgroundColor': '#013e48',
                    'borderBottom': '2px solid #025059',
                    'gap': '15px'  # Space between links
                }
            )
        ],
        style={
            'backgroundColor': '#013e48',
            'color': '#ffffff',
            'marginBottom': '1%',
            'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'  # Add subtle shadow for depth
        }
    )
