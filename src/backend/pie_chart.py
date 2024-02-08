from pandas import DataFrame
from plotly.graph_objects import Pie
from plotly.subplots import make_subplots

def get_dto_dount(filtered_data):
    pie_chart = filtered_data.drop_duplicates(['model_id', 'molecular_characterisation_type']).groupby(
        'molecular_characterisation_type').count()['model_id']
    colors_dict = {'mutation': '#ef553b', 'expression': '#636efa', 'copy number alteration': '#b6e880',
              'images': '#00cc96', 'drug': '#19d3f3', 'treatment': '#ff6692',
              'immunemarker': '#ffa15a', 'biomarker': '#ab63fa'}
    categories = pie_chart.index.name
    columns = [categories, 'counts']
    data_counts = DataFrame(zip(list(pie_chart.index), list(pie_chart)), columns=columns).sort_values(categories).reset_index(drop=True)
    label = pie_chart.index.str.title()
    '''
    theta = linspace(0, 2 * pi, pie_chart.max(), endpoint=False)
    theta = concatenate((theta, [theta[0]]))  # Close the circle
    '''
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
            values=[pie_chart[dt], pie_chart.max()-pie_chart[dt]],
            name=dt,
            hoverinfo='label+percent+value',
            hole=0.4,
            marker_colors=[colors_dict[str(dt).lower()], '#ffffff']
        ), row=row, col=col)
        if i == cols:
            row=2

        '''
        fig.add_trace(go.Scatterpolar(
            r=list(range(radius, pie_chart[dt])),
            theta=theta,
            mode='lines',
            name=dt,
            line_color=colors_dict[str(dt).lower()]
        ))
        radius +=5
        '''
    '''
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False),
            angularaxis=dict(direction='clockwise'),
        ),
    )
    '''
    #fig = go.Figure(go.Bar(x=pie_chart[categories], y=pie_chart['counts'], hoverinfo='text',
    #                       marker_color=[colors_dict[str(l).lower()] for l in label], text=label))
    #fig = go.Figure(go.Pie(labels=label, values=pie_chart['counts'], marker_colors=[colors_dict[str(l).lower()] for l in label]))
    #fig.update_traces(hole=0.4)
    return fig
