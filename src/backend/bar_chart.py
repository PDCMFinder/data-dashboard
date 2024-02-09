from pandas import DataFrame, read_csv, concat
from src.resources import total_models, labels, reactive_categories
from plotly.graph_objects import Figure, Bar

def get_bar_chart():
    models = DataFrame()
    for f in total_models.keys():
        file = total_models[f]
        model = read_csv(file, usecols=['model_id', 'provider']).drop_duplicates()
        model['Release'] = labels[f]
        models = concat([models, model])
    models = models.groupby('Release').count().to_dict()['model_id']
    models = DataFrame(list(models.items()), columns=['Release', 'Models'])
    fig = Figure(data=[Bar(x=models['Release'], y=models['Models'], marker_color='#013e48')])
    fig.update_layout(
        title=dict(text="Model Distribution per Data Release", yref='container')
    )
    return fig

def get_reactive_bar_plot(data, column):
    data = data.groupby(column).count().to_dict()['model_id']
    data = DataFrame(list(data.items()), columns=[column, 'Models'])
    if column == 'model_type':
        data[column] = ['Organoid' if str(t).lower().__contains__('organoid') else t for t in data[column]]
        data[column] = [
            'Cell Line' if str(t).lower().__contains__('cell') or str(t).lower().__contains__('pdc') or str(
                t).lower().__contains__('2d') or str(t).lower().__contains__('2-d') else t for t in data[column]]
        data[column] = [
            'Other' if str(t).lower().__contains__('other') or str(t).lower().__contains__('mixed') else t for t in
            data[column]]
    fig = Figure(data=[Bar(x=data[column], y=data['Models'])])
    if len(data[column]) > 15:
        fig.update_layout(
            xaxis=dict(
                tickfont=dict(size=9)
            ),
            title=dict(text=f"Bar plot showing models grouped by {get_key_from_value(reactive_categories, column).title()}",
                       yref="container"),
        )
    return fig


def get_key_from_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None