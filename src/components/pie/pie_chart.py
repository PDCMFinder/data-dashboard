import pandas as pd
from plotly.graph_objects import Pie, Scatterpolar, Figure
from plotly.subplots import make_subplots
from numpy import linspace, arange, isnan


def get_dto_donut(filtered_data, tm):
    pie_chart = filtered_data.drop_duplicates(['model_id', 'molecular_characterisation_type']).groupby(
        'molecular_characterisation_type').count().sort_index()['model_id']
    colors_dict = {'mutation': '#ef553b', 'expression': '#636efa', 'copy number alteration': '#b6e880',
              'images': '#00cc96', 'drug': '#19d3f3', 'treatment': '#ff6692',
              'immunemarker': '#ffa15a', 'biomarker': '#ab63fa'}
    cols = 4#int(len(pie.index)/2)
    fig = make_subplots(rows=2, cols=cols,
                        specs=[[{"type": "pie"}]*cols, [{"type": "pie"}]*cols])
    row = 1
    for i, dt in enumerate(pie_chart.index, 1):
        if row == 1 and i <= cols:
            col = i
        else:
            col = int(i - 4)
        fig.add_trace(Pie(
            labels=[dt, 'No data'],
            values=[pie_chart[dt], tm-pie_chart[dt]],
            name=dt,
            hoverinfo='label+percent+value',
            hole=0.4,
            marker_colors=[colors_dict[str(dt).lower()], '#ffffff']
        ), row=row, col=col)
        if i == cols:
            row=2

    return fig


def get_model_type_donut(df):
    labels = df['model_type'].tolist()
    values = df['model_count'].tolist()
    color_code = {"PDX": "#6e9eeb", "Organoid": "#8f7cc3", "Cell Line": "#94c37e", "Other": "#ea921b"}
    colors = [color_code[label] for label in labels]

    fig = Figure(data=[Pie(labels=labels, values=values, hole=0.4, marker=dict(colors=colors))])

    return fig


def get_dto_radial(pie_chart, tm):
    colors_dict = {'mutation': '#ef553b', 'expression': '#636efa', 'copy number alteration': '#b6e880',
              'images': '#00cc96', 'drug': '#19d3f3', 'treatment': '#ff6692',
              'immunemarker': '#ffa15a', 'biomarker': '#ab63fa', 'publication': '#ffda2f'}
    fig = Figure()
    radius = 0
    for i, row in pie_chart.iterrows():
        dt = row.iloc[0]
        count = row.iloc[1]
        if not isnan(count):
            theta = linspace(0, 360 * (count/tm), count, endpoint=False)
            fig.add_trace(Scatterpolar(
                r=arange(radius, count, 0.01),
                theta=theta,
                mode='lines',
                name=dt,
                line=dict(width=5),
                hovertemplate=f'models: {count}, percentage: {round(count/tm*100, 2)}',
                line_color=colors_dict[str(dt).lower()]
            ))
            radius+=225

    fig.update_layout(
        polar=dict(
            radialaxis=dict(range=[0, len(pie_chart.index)*260], visible=False, showgrid=False, showticklabels=False,),
            angularaxis=dict(showline=False, showticklabels=False, direction='clockwise'),
        ),
    )
    return fig


def get_library_strategy_plot(df):
    molecular_characterisation_type = ['mutation', 'expression', 'copy number alteration']
    fig = make_subplots(rows=1, cols=3, specs=[[{"type": "pie"}] * 3])
    col = 1
    color_map = {"WES": "#636EFA", "WGS": "#EF553B",
                 "Targeted": "#00CC96", "RNA-Seq": "#AB63FA",
                 "Microarray": "#FFA15A", "Not provided": "#19D3F3", "NGS": "#FF6692", "Not Provided": "#19D3F3"}
    for mct in molecular_characterisation_type:
        temp = df[df['molecular_characterisation_type'] == mct].reset_index(drop=True)
        labels = temp['library_strategy'].tolist()
        values = temp['model_count'].tolist()
        cmap = [color_map[l] for l in labels]
        fig.add_trace(Pie(labels=labels, values=values, name=mct.title(), marker=dict(colors=cmap)), row=1, col=col)
        col += 1
    return fig
