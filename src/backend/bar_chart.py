from pandas import DataFrame, read_csv, concat
from src.resources import total_models, labels
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
    return fig
