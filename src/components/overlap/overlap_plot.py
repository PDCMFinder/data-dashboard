import numpy as np
import pandas as pd
from plotly_upset.plotting import plot_upset


def overlap_diagram(df, width):
    # Plotting
    fig = plot_upset(
        dataframes=[df],
        legendgroups=["All models"],
        marker_size=10,
        exclude_zeros=True,
        sorted_x="d",
        sorted_y="a",
        column_widths=[0.2, 0.8],
        vertical_spacing=0.,
        horizontal_spacing=0.05,
        row_heights=[0.6, 0.4],
    )

    fig.update_layout(
        width=width-10,
        height=width/1.5,
    )
    return fig