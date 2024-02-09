from pandas import DataFrame
from plotly.graph_objects import Pie, Scatterpolar, Figure, Layout
from plotly.subplots import make_subplots
from numpy import linspace, concatenate, pi, arange

def get_dto_donut(filtered_data, tm):
    pie_chart = filtered_data.drop_duplicates(['model_id', 'molecular_characterisation_type']).groupby(
        'molecular_characterisation_type').count().sort_index()['model_id']
    colors_dict = {'mutation': '#ef553b', 'expression': '#636efa', 'copy number alteration': '#b6e880',
              'images': '#00cc96', 'drug': '#19d3f3', 'treatment': '#ff6692',
              'immunemarker': '#ffa15a', 'biomarker': '#ab63fa'}
    cols = 4#int(len(pie_chart.index)/2)
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
    df['model_type'] = ['Organoid' if str(t).lower().__contains__('organoid') else t for t in df['model_type']]
    df['model_type'] = ['Cell Line' if str(t).lower().__contains__('cell') or str(t).lower().__contains__('pdc') or str(t).lower().__contains__('2d') or str(t).lower().__contains__('2-d') else t for t in df['model_type']]
    df['model_type'] = ['Other' if str(t).lower().__contains__('other') or str(t).lower().__contains__('mixed') else t for t in df['model_type']]

    df = df.groupby('model_type').count()['provider']
    labels = df.index.tolist()
    values = df.values.tolist()
    fig = Figure(data=[Pie(labels=labels, values=values, hole=0.4)])
    fig.update_layout(
        title=dict(text="Model type overview", automargin=True, yref='container')
    )
    return fig


def get_dto_radial(filtered_data, tm):
    pie_chart = filtered_data.drop_duplicates(['model_id', 'molecular_characterisation_type']).groupby(
        'molecular_characterisation_type').count().sort_index()['model_id']
    colors_dict = {'mutation': '#ef553b', 'expression': '#636efa', 'copy number alteration': '#b6e880',
              'images': '#00cc96', 'drug': '#19d3f3', 'treatment': '#ff6692',
              'immunemarker': '#ffa15a', 'biomarker': '#ab63fa'}

    fig = Figure()
    radius = 0
    for i, dt in enumerate(pie_chart.index, 1):
        theta = linspace(0, 360 * (pie_chart[dt]/tm), pie_chart[dt], endpoint=False)
        fig.add_trace(Scatterpolar(
            r=arange(radius, pie_chart[dt], 0.1),
            theta=theta,
            mode='lines',
            name=dt,
            line=dict(width=5),
            hovertemplate=f'models: {pie_chart[dt]}, percentage: {round(pie_chart[dt]/tm*100, 2)}',
            line_color=colors_dict[str(dt).lower()]
        ))
        radius +=250

    fig.update_layout(
        polar=dict(
            radialaxis=dict(range=[0, len(pie_chart.index)*260], visible=False, showgrid=False, showticklabels=False,),
            angularaxis=dict(showline=False, showticklabels=False, direction='clockwise'),
        ),
        title=dict(text="Data type overview", automargin=True, yref='container')
    )
    return fig


def get_library_strategy_plot(df):
    df['library_strategy'] = df['library_strategy'].fillna('Not Provided').astype(str).str.replace('mRNA NGS', 'RNA-Seq').replace('WXS', 'WES').replace('microarray', 'Microarray')
    df['library_strategy'] = ['Targeted' if str(t).lower().__contains__('target') else t for t in df['library_strategy']]

    df = df.groupby(['molecular_characterisation_type', 'library_strategy']).count()['model_id']
    molecular_characterisation_type = ['mutation', 'expression', 'copy number alteration']
    fig = make_subplots(rows=1, cols=3, specs=[[{"type": "pie"}] * 3])
    col = 1
    for mct in molecular_characterisation_type:
        labels = df[mct].index.tolist()
        values = df[mct].values.tolist()
        fig.add_trace(Pie(labels=labels, values=values, name=mct.title()), row=1, col=col)
        col += 1
    fig.update_layout(
        title=dict(text="Technology used for each data type", automargin=True, yref='paper')
    )
    return fig