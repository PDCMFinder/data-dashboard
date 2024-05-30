import pandas as pd
from pandas import DataFrame, read_csv, read_json, notna, concat
from src.backend.pie_chart import get_model_type_donut, get_dto_radial, get_library_strategy_plot
from src.backend.venn import get_dt_venn, get_venn_table
from src.backend.scatter import get_scatter_plot
from src.backend.bar_chart import get_bar_chart, get_reactive_bar_plot, get_country_bar_plot, get_molecular_model_type_plot
from src.resources import input_file, total_models, labels
from requests import get

data = DataFrame([[0, 0], [1, 1]], columns=['Type', 'Model'])
country = DataFrame(columns=['country', 'provider'])
summary = DataFrame(columns=['tag', 'date', "model_type_pdx", "model_type_cell_line", "model_type_organoid", "model_type_other", "model_type_total", "sample_type_xenograft", "sample_type_cell", "sample_type_patient", "sample_type_total", "molecular_data_biomarker", "molecular_data_cna", "molecular_data_expression", "molecular_data_immunemarker", "molecular_data_mut", "molecular_data_points_total", "drug_data_points", "treatment_data_points", "image_data_points"])

def custom_plots(selected_category, selected_plot):
    file = input_file[selected_category]
    if selected_category == 'latest':
        mapper = {'data_source': 'provider', 'data_type': 'molecular_characterisation_type',
                  'platform_name': 'instrument_model'}
        data_overview = read_json(file).rename(columns=mapper)
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
            temp = temp[data_overview.columns]
            data_overview = concat([data_overview, temp]).reset_index(drop=True)
        data_overview['molecular_characterisation_type'] = data_overview['molecular_characterisation_type'].str.replace('bio markers', 'biomarker')
    else:
        data_overview = read_csv(file)
    if selected_plot == 'dto_donut':
        if selected_category == 'latest':
            mapper = {'data_source': 'provider', 'type': 'model_type', 'pubmed_ids': 'publications',
                      'patient_age': 'age_in_years_at_collection', 'histology': 'diagnosis', 'patient_sex': 'sex',
                      'patient_ethnicity': 'ethnicity'}
            tm = read_json(total_models[selected_category]).rename(columns=mapper).shape[0]
        else:
            tm = read_csv(total_models[selected_category]).shape[0]
        fig = get_dto_radial(data_overview, int(tm))
        return fig
    elif selected_plot == 'dt_venn':
        fig, table_data = get_dt_venn(data_overview)
        table_display = {'display': 'block', 'marginTop': '10px'}
        return fig, table_display, table_data.to_dict('records')
    elif selected_plot == "library_strategy":
        return get_library_strategy_plot(data_overview)
    if selected_plot == 'table':
        model = read_csv(total_models[selected_category])
        return get_venn_table(data_overview, f"assets/exports/{selected_category}_mol_data_model_list.xlsx", model)

def bar_chart():
    return get_bar_chart()

def cancer_system_plot(category):
    file = total_models[category]
    if category == 'latest':
        mapper = {'data_source': 'provider', 'type': 'model_type', 'pubmed_ids': 'publications',
                  'patient_age': 'age_in_years_at_collection', 'histology': 'diagnosis', 'patient_sex': 'sex',
                  'patient_ethnicity': 'ethnicity'}
        data = read_json(file).rename(columns=mapper)
    else:
        data = read_csv(file)
    return get_scatter_plot(data)

def model_type_pie(category):
    file = total_models[category]
    if category == 'latest':
        mapper = {'data_source': 'provider', 'type': 'model_type', 'pubmed_ids': 'publications',
                  'patient_age': 'age_in_years_at_collection', 'histology': 'diagnosis', 'patient_sex': 'sex',
                  'patient_ethnicity': 'ethnicity'}
        data = read_json(file).rename(columns=mapper)
    else:
        data = read_csv(file)
    return get_model_type_donut(data.drop_duplicates(['model_id']))

def reactive_bar_plot(release, category, gc):
    file = total_models[release]
    if release == 'latest':
        mapper = {'data_source': 'provider', 'type': 'model_type', 'pubmed_ids': 'publications',
                  'patient_age': 'age_in_years_at_collection', 'histology': 'diagnosis', 'patient_sex': 'sex',
                  'patient_ethnicity': 'ethnicity'}
        data = read_json(file).rename(columns=mapper)
    else:
        data = read_csv(file)
    return get_reactive_bar_plot(data, category, gc)

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
            file_name = f"assets/phenomic/phenomics_data_points_{f['tag_name'].replace('PDCM_', '')}.csv"
            df = read_csv(file_name).groupby('release').sum().reset_index()
            file_name = f"assets/model/total_models_{f['tag_name'].replace('PDCM_', '')}.csv"
            data = read_csv(file_name)
            data['model_type'] = ['Organoid' if str(t).lower().__contains__('organoid') else t for t in
                                  data['model_type']]
            data['model_type'] = [
                'Cell Line' if str(t).lower().__contains__('cell') or str(t).lower().__contains__('pdc') or str(
                    t).lower().__contains__('2d') or str(t).lower().__contains__('2-d') else t for t in
                data['model_type']]
            data['model_type'] = [
                'Other' if str(t).lower().__contains__('other') or str(t).lower().__contains__('mixed') else t for t in
                data['model_type']]
            data = data.groupby('model_type').count()['model_id'].reset_index()
            df['model_type_cell_line'] = data[data['model_type'].str.contains('Cell')].reset_index(drop=True)['model_id'][0]
            df['model_type_organoid'] = data[data['model_type'].str.contains('Organoid')].reset_index(drop=True)['model_id'][0]
            df['model_type_pdx'] = data[data['model_type'].str.contains('PDX')].reset_index(drop=True)['model_id'][0]
            df['model_type_other'] = data[data['model_type'].str.contains('Other')].reset_index(drop=True)['model_id'][0]
            df['model_type_total'] = data['model_id'].sum()

            df['date'] = f['released_at'].split('T')[0]
            df['tag'] = labels[f['tag_name'].replace('PDCM_', '').replace('v', '')]
            table = pd.concat([table, df]).reset_index(drop=True)
    return table.to_dict('records')


def generate_country_plot(release):
    file_name = f"assets/country/provider_country_{release.replace('DR_', 'DR_v')}.csv"
    table = read_csv(file_name).rename({'0':'release', '1':'provider', '2':'country'}, axis=1)[['country', 'provider']]
    df = table.groupby('country')['provider'].apply(list).reset_index(name='provider')
    df['provider'] = df['provider'].astype(str)
    return get_country_bar_plot(table), df.to_dict('records')

def molecular_model_type_plot(release):
    file = input_file[release]
    df_2 = read_csv(file)

    file = total_models[release]
    df = read_csv(file)
    df.loc[:, 'model_type'] = ['Organoid' if str(t).lower().__contains__('organoid') else t for t in df['model_type']]
    df.loc[:, 'model_type'] = [
        'Cell Line' if str(t).lower().__contains__('cell') or str(t).lower().__contains__('pdc') or str(
            t).lower().__contains__('2d') or str(t).lower().__contains__('2-d') else t for t in df['model_type']]
    df.loc[:, 'model_type'] = [
        'Other' if str(t).lower().__contains__('other') or str(t).lower().__contains__('mixed') else t for t in
        df['model_type']]

    temp = df_2.drop_duplicates(['molecular_characterisation_type', 'model_id'])[['model_id', 'molecular_characterisation_type']].merge(df[['model_id', 'model_type']],
                                                                         on='model_id', how='left')
    return get_molecular_model_type_plot(temp)