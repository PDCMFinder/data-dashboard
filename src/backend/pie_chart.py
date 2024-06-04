from pandas import DataFrame
from plotly.graph_objects import Pie, Scatterpolar, Figure, Layout
from plotly.subplots import make_subplots
from numpy import linspace, concatenate, pi, arange
from plotly.express.colors import qualitative

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
    df = df.groupby('model_type').count()['provider']
    labels = df.index.tolist()
    values = df.values.tolist()
    color_code = {"PDX": "#6e9eeb", "Organoid": "#8f7cc3", "Cell Line": "#94c37e", "Other": "#ea921b"}
    colors = [color_code[label] for label in labels]

    fig = Figure(data=[Pie(labels=labels, values=values, hole=0.4, marker=dict(colors=colors))])

    return fig


def get_dto_radial(filtered_data, tm):
    pie_chart = filtered_data.drop_duplicates(['model_id', 'molecular_characterisation_type']).groupby(
        'molecular_characterisation_type').count().sort_index()['model_id'].sort_values()
    colors_dict = {'mutation': '#ef553b', 'expression': '#636efa', 'copy number alteration': '#b6e880',
              'images': '#00cc96', 'drug': '#19d3f3', 'treatment': '#ff6692',
              'immunemarker': '#ffa15a', 'biomarker': '#ab63fa'}

    fig = Figure()
    radius = 0
    for i, dt in enumerate(pie_chart.index):
        theta = linspace(0, 360 * (pie_chart[dt]/tm), pie_chart[dt], endpoint=False)
        fig.add_trace(Scatterpolar(
            r=arange(radius, pie_chart[dt], 0.01),
            theta=theta,
            mode='lines',
            name=dt,
            line=dict(width=5),
            hovertemplate=f'models: {pie_chart[dt]}, percentage: {round(pie_chart[dt]/tm*100, 2)}',
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
    replacements = {'Not Provided': 'Not provided',
                    'Immunohistochemistry': 'IHC', 'immunohistochemistry': 'IHC',
                    'Tumor mutation burden': 'Tumor Mutation Burden',
                    'Illumina microarray': 'Microarray', 'arraw comparative genomic hybridization': 'Microarray',
                    'Genomic plateform of Curie Institute': 'Microarray', 'aCGH array 2x400k': 'Microarray', 'aCGH array 4x180k': 'Microarray',
                    'whole exome sequencing': 'WES', 'Whole exome sequencing': 'WES',
                    'NGS plateform of Curie Institute': 'NGS',
                    'rna sequencing': 'RNA-Seq', 'RNA sequencing': 'RNA-Seq', 'RNAseq': 'RNA-Seq',
                    'Illumina HT-12 v3': 'WGS', 'NGS': 'NGS', }
    df['library_strategy'] = df['library_strategy'].replace(replacements)
    df = df.groupby(['molecular_characterisation_type', 'library_strategy']).count()['model_id']
    molecular_characterisation_type = ['mutation', 'expression', 'copy number alteration']
    fig = make_subplots(rows=1, cols=3, specs=[[{"type": "pie"}] * 3])
    col = 1
    color_map = {"WES": "#636EFA", "WGS": "#EF553B",
                 "Targeted": "#00CC96", "RNA-Seq": "#AB63FA",
                 "Microarray": "#FFA15A", "Not provided": "#19D3F3", "NGS": "#FF6692"}
    for mct in molecular_characterisation_type:
        labels = df[mct].index.tolist()
        values = df[mct].values.tolist()
        cmap = [color_map[l] for l in labels]
        fig.add_trace(Pie(labels=labels, values=values, name=mct.title(), marker=dict(colors=cmap)), row=1, col=col)
        col += 1
    return fig
