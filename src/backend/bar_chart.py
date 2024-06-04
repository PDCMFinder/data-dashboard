from pandas import DataFrame, read_csv, concat, read_json
from src.resources import labels, reactive_categories, primary_site_mapping, cancer_system, diagnosis_to_cancer
from src.transform import read_input_file
from plotly_express import bar


def get_bar_chart():
    models = DataFrame()
    for f in labels.keys():
        if f != 'latest':
            model = read_input_file(f"assets/model/total_models_{f.replace('_', '_v')}.csv", ['model_id', 'provider', 'model_type']).drop_duplicates()
        else:
            mapper = {'data_source': 'provider', 'type': 'model_type', 'pubmed_ids': 'publications',
                      'patient_age': 'age_in_years_at_collection', 'histology': 'diagnosis', 'patient_sex': 'sex',
                      'patient_ethnicity': 'ethnicity'}
            url = ''
            model = read_json(url).rename(columns=mapper)
        model = model.groupby('model_type').count()['model_id']
        model = DataFrame(zip(model.index.tolist(), model.values.tolist()), columns=['Model Type', 'Model Count'])
        model['Release'] = labels[f]
        models = concat([models, model]).reset_index(drop=True)
    models = models.iloc[::-1]
    total = models.groupby('Release').sum()['Model Count'].to_dict()
    models['Total Models'] = [total[r] for r in models['Release']]
    color_code = {"PDX": "#6e9eeb", "Organoid": "#8f7cc3", "Cell Line": "#94c37e", "Other": "#ea921b"}
    fig = bar(models, x='Release', y='Model Count', color='Model Type', hover_data=['Total Models'], color_discrete_map=color_code)
    fig.update_layout(
        title=dict(text="Model Distribution per Data Release", yref='container')
    )
    return fig


def get_reactive_bar_plot(data, column, gc):
    color_code = {"PDX": "#6e9eeb", "Organoid": "#8f7cc3", "Cell Line": "#94c37e", "Other": "#ea921b"}
    if gc is None or column == gc:
        fig = bar(data, x=column, y='Count', color_discrete_map=color_code)
    else:
        data = data.sort_values(by=gc)
        total = data.groupby(column).sum()['Count'].to_dict()
        data['Total'] = [total[r] for r in data[column]]
        fig = bar(data, x=column, y='Count', color=gc, hover_name=gc, hover_data='Total', color_discrete_map=color_code)
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        for trace in fig.data:
            trace.update(showlegend=False)
    if len(data[column]) > 15:
        fig.update_layout(
            xaxis=dict(
                tickfont=dict(size=9)
            ),
        )
    fig.update_layout(
        title=dict(text=f"Model counts for attribute {get_key_from_value(reactive_categories, column).title()}",
                   yref="container"),
    )
    return fig


def get_key_from_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None

def get_country_bar_plot(df):
    fig = bar(df.groupby('country').count()['provider'].reset_index(), x='country', y='provider')
    return fig


def get_molecular_model_type_plot(data):
    color_code = {"PDX": "#6e9eeb", "Organoid": "#8f7cc3", "Cell Line": "#94c37e", "Other": "#ea921b"}

    fig = bar(data, x='molecular_characterisation_type', y='Count', color='model_type', hover_name='model_type',
              hover_data='Total', color_discrete_map=color_code)
    return fig