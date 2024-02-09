from pandas import DataFrame, read_csv, concat
from src.resources import total_models, labels, reactive_categories
from plotly.graph_objects import Figure, Bar
from plotly_express import bar

def get_bar_chart():
    models = DataFrame()
    for f in total_models.keys():
        file = total_models[f]
        model = read_csv(file, usecols=['model_id', 'provider', 'model_type']).drop_duplicates()
        model['model_type'] = ['Organoid' if str(t).lower().__contains__('organoid') else t for t in model['model_type']]
        model['model_type'] = [
            'Cell Line' if str(t).lower().__contains__('cell') or str(t).lower().__contains__('pdc') or str(
                t).lower().__contains__('2d') or str(t).lower().__contains__('2-d') else t for t in model['model_type']]
        model['model_type'] = [
            'Other' if str(t).lower().__contains__('other') or str(t).lower().__contains__('mixed') else t for t in
            model['model_type']]
        model = model.groupby('model_type').count()['model_id']
        model = DataFrame(zip(model.index.tolist(), model.values.tolist()), columns=['Model Type', 'Model Count'])
        model['Release'] = labels[f]
        models = concat([models, model]).reset_index(drop=True)
    models = models.iloc[::-1]
    total = models.groupby('Release').sum()['Model Count'].to_dict()
    models['Total Models'] = [total[r] for r in models['Release']]
    fig = bar(models, x='Release', y='Model Count', color='Model Type', hover_data=['Total Models'])
    fig.update_layout(
        title=dict(text="Model Distribution per Data Release", yref='container')
    )
    return fig

def get_reactive_bar_plot(data, column):
    if column == 'publications':
        data[column] = data[column].fillna('No')
        data[column] = ['Yes' if str(p).__contains__('PMID') else 'No' for p in data[column]]
    if column == 'age_in_years_at_collection':
        data[column] = ['Younger than 21' if not str(a).lower().__contains__('not') and float(a) < 21 else 'Not provided' if str(a).lower().__contains__('not') else 'Older than 21' for a in data[column]]
    if column == 'sex' or column == 'ethnicity':
        data[column] = data[column].str.title()
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