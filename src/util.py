import pandas as pd
from pandas import DataFrame, read_csv, read_json, notna, concat
from src.backend.pie_chart import get_model_type_donut, get_dto_radial, get_library_strategy_plot
from src.backend.venn import get_dt_venn, get_dt_venn4, get_venn_table
from src.backend.bar_chart import get_bar_chart, get_reactive_bar_plot, get_country_bar_plot, get_molecular_model_type_plot
from src.resources import labels
from src.transform import load_data
from requests import get

data = DataFrame([[0, 0], [1, 1]], columns=['Type', 'Model'])
country = DataFrame(columns=['country', 'provider'])
summary = DataFrame(columns=['tag', 'date', "model_type_pdx", "model_type_cell_line", "model_type_organoid", "model_type_other", "model_type_total", "sample_type_xenograft", "sample_type_cell", "sample_type_patient", "sample_type_total", "molecular_data_biomarker", "molecular_data_cna", "molecular_data_expression", "molecular_data_immunemarker", "molecular_data_mut", "molecular_data_points_total", "drug_data_points", "treatment_data_points", "image_data_points"])

def custom_plots(release, plot_type, export_type='plot'):
    if release == 'latest':
        url = 'https://www.cancermodels.org/api/model_molecular_metadata?select=sample_id,data_source,data_type,platform_name,model_id'
        mapper = {'data_source': 'provider', 'data_type': 'molecular_characterisation_type',
                  'platform_name': 'instrument_model'}
        samples = read_json(url).rename(columns=mapper)
        immune_image_data = read_json('https://www.cancermodels.org/api/search_index?select=patient_sample_id,data_source,dataset_available,model_images,external_model_id')
        immune_image_data['model_images'] = [None if r is None else 'images' for r in immune_image_data['model_images']]
        immune_image_data['immunemarker'] = ['immunemarker' if r is not None and 'immune markers' in r else None for r in immune_image_data['dataset_available']]
        immune_image_data['treatment'] = ['treatment' if r is not None and 'patient treatment' in r else None for r in immune_image_data['dataset_available']]
        immune_image_data['drug'] = ['drug' if r is not None and 'dosing studies' in r else None for r in immune_image_data['dataset_available']]
        for t in ['model_images', 'treatment', 'drug', 'immunemarker']:
            temp = immune_image_data[~immune_image_data[t].isna()]
            temp['provider'] = temp['data_source']
            temp['molecular_characterisation_type'] = temp[t]
            temp['instrument_model'] = ""
            temp['sample_id'] = temp['patient_sample_id']
            temp['model_id'] = temp['external_model_id']
            temp = temp[samples.columns]
            samples = concat([samples, temp]).reset_index(drop=True)
        samples['molecular_characterisation_type'] = samples['molecular_characterisation_type'].str.replace('bio markers', 'biomarker')
    else:
        samples = load_data(release)['samples']
    if plot_type == 'dto_donut':
        if release == 'latest':
            url = 'https://www.cancermodels.org/api/model_metadata?select=model_id,data_source,type,pubmed_ids,patient_age,histology,tumor_type,primary_site,patient_sex,patient_ethnicity'
            mapper = {'data_source': 'provider', 'type': 'model_type', 'pubmed_ids': 'publications',
                      'patient_age': 'age_in_years_at_collection', 'histology': 'diagnosis', 'patient_sex': 'sex',
                      'patient_ethnicity': 'ethnicity'}
            tm = read_json(url).rename(columns=mapper).shape[0]
        else:
            tm = load_data(release)['total'][['model_id']].shape[0]
        if export_type == 'table':
            return samples.drop_duplicates(['model_id', 'molecular_characterisation_type']).groupby(
        'molecular_characterisation_type').count().sort_index()['model_id'].sort_values().reset_index()
        fig = get_dto_radial(samples, int(tm))
        return fig
    elif plot_type.__contains__('dt_venn'):
        plot_type = plot_type.split('_')[-1]
        models = load_data(release)['total'][['model_id', 'provider', 'model_type']]
        if plot_type != 'Total' and plot_type != 'venn':
            models = models[models['model_type'] == plot_type]
            samples = samples[['sample_id', 'provider', 'molecular_characterisation_type', 'model_id']].merge(models, on=[
                'model_id', 'provider'], how='inner')
        if export_type == 'table':
            return get_venn_table(samples, f"assets/exports/{release}_mol_data_model_list.xlsx", models)
        return get_dt_venn(samples, plot_type)
    elif plot_type == 'dt_v4venn':
        if export_type == 'biomarker':
            return get_dt_venn4(samples, 'bio')
        return get_dt_venn4(samples)

    elif plot_type == "library_strategy":
        samples['library_strategy'] = samples['library_strategy'].fillna('Not Provided').astype(str).str.replace('mRNA NGS',
                                                                                                       'RNA-Seq').replace(
            'WXS', 'WES').replace('microarray', 'Microarray')
        samples['library_strategy'] = ['Targeted' if str(t).lower().__contains__('target') else t for t in
                                  samples['library_strategy']]
        if export_type == 'table':
            return samples.groupby(['molecular_characterisation_type', 'library_strategy']).count()['model_id'].reset_index()
        return get_library_strategy_plot(samples)


def bar_chart():
    models = DataFrame()
    for f in labels.keys():
        if f != 'latest':
            model = load_data(f)['total'][['model_id', 'provider', 'model_type']].drop_duplicates(subset=['model_id'])
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
    return get_bar_chart(models)

def model_type_pie(release, type):
    if release == 'latest':
        url = 'https://www.cancermodels.org/api/model_metadata?select=model_id,data_source,type,pubmed_ids,patient_age,histology,tumor_type,primary_site,patient_sex,patient_ethnicity'
        mapper = {'data_source': 'provider', 'type': 'model_type', 'pubmed_ids': 'publications',
                  'patient_age': 'age_in_years_at_collection', 'histology': 'diagnosis', 'patient_sex': 'sex',
                  'patient_ethnicity': 'ethnicity'}
        models = read_json(url).rename(columns=mapper)
    else:
        models = load_data(release)['total'][['model_id', 'provider', 'model_type']]
    if type == 'plot':
        return get_model_type_donut(models.drop_duplicates(['model_id']))
    else:
        return models.drop_duplicates(['model_id']).groupby('model_type').count()['provider'].reset_index()

def reactive_bar_plot(release, category, gc, plot_type):
    if release == 'latest':
        url = 'https://www.cancermodels.org/api/model_metadata?select=model_id,data_source,type,pubmed_ids,patient_age,histology,tumor_type,primary_site,patient_sex,patient_ethnicity'
        mapper = {'data_source': 'provider', 'type': 'model_type', 'pubmed_ids': 'publications',
                  'patient_age': 'age_in_years_at_collection', 'histology': 'diagnosis', 'patient_sex': 'sex',
                  'patient_ethnicity': 'ethnicity'}
        models = read_json(url).rename(columns=mapper)
    else:
        models = load_data(release)['total']
    groupby_columns = [category]
    if gc is not None and category != gc:
        groupby_columns.append(gc)
    models = models.groupby(groupby_columns).size().reset_index(name='Count').sort_values(by=category)
    models = models[models[category] != "Not provided"]
    if plot_type == 'table':
        return models
    return get_reactive_bar_plot(models, category, gc)

def process_values(value):
    if notna(value):
        # Convert the string representation of list to actual list
        value_list = eval(value)
        # Remove specified elements from the list
        value_list = [v for v in value_list if v not in ['mutation', 'copy number alteration', 'expression']]
        # Return a list of dictionaries with one entry for each value in the modified list
        return [{'value': v} for v in value_list]
    else:
        return None

def generate_summary_stats():
    table = DataFrame()
    for f in get("https://gitlab.ebi.ac.uk/api/v4/projects/1629/releases?private_token=glpat-gbQzKFxHTWyp_jZhP5gE").json():
        if f['tag_name'].replace('PDCM_', '').replace('v', '') in labels.keys():
            df = read_csv(f"assets/phenomic/phenomics_data_points_{f['tag_name'].replace('PDCM_', '')}.csv").groupby('release').sum(numeric_only=False).reset_index()
            data = load_data(f['tag_name'].replace('PDCM_DR_v', 'DR_'))['total'][['model_id', 'model_type']].groupby('model_type').count()['model_id'].reset_index()
            df['model_type_cell_line'] = data[data['model_type'].str.contains('Cell')].reset_index(drop=True)['model_id'][0]
            df['model_type_organoid'] = data[data['model_type'].str.contains('Organoid')].reset_index(drop=True)['model_id'][0]
            df['model_type_pdx'] = data[data['model_type'].str.contains('PDX')].reset_index(drop=True)['model_id'][0]
            df['model_type_other'] = data[data['model_type'].str.contains('Other')].reset_index(drop=True)['model_id'][0]
            df['model_type_total'] = data['model_id'].sum()

            df['date'] = f['released_at'].split('T')[0]
            df['tag'] = labels[f['tag_name'].replace('PDCM_', '').replace('v', '')]
            table = pd.concat([table, df]).reset_index(drop=True)
    return table.to_dict('records')


def generate_country_plot(release, plot_type):
    table = load_data(release)['country'].rename({'0':'release', '1':'provider', '2':'country'}, axis=1)[['country', 'provider']]
    df = table.groupby('country')['provider'].apply(list).reset_index(name='provider')
    df['provider'] = df['provider'].astype(str)
    if plot_type == 'table':
        return table.groupby('country').count()['provider'].reset_index()
    return get_country_bar_plot(table), df.to_dict('records')

def molecular_model_type_plot(release, plot_type):
    df_2 = load_data(release)['samples']
    df = load_data(release)['total'][['model_id', 'model_type']]
    temp = df_2.drop_duplicates(['molecular_characterisation_type', 'model_id'])[['model_id', 'molecular_characterisation_type']].merge(df,
                                                                         on='model_id', how='left')
    data = temp.groupby(['molecular_characterisation_type', 'model_type']).size().reset_index(name='Count')
    total = data.groupby('molecular_characterisation_type').sum(numeric_only=False)['Count'].to_dict()
    data['Total'] = [total[r] for r in data['molecular_characterisation_type']]
    if plot_type == 'table':
        return data
    return get_molecular_model_type_plot(data)


class get_release_data:
    def __init__(self, release):
        self.release = release
    def read_data(self):
        self.df = "Data"