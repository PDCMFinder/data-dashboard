from pandas import DataFrame, read_csv, read_json, notna, concat
from src.backend.pie_chart import get_model_type_donut, get_dto_radial, get_library_strategy_plot
from src.backend.venn import get_dt_venn
from src.backend.scatter import get_scatter_plot
from src.backend.bar_chart import get_bar_chart, get_reactive_bar_plot
from src.resources import input_file, total_models

data = DataFrame([[0, 0], [1, 1]], columns=['Type', 'Model'])


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
    if selected_plot == 'dt_venn':
        fig, table_data = get_dt_venn(data_overview)
        table_display = {'display': 'block', 'marginTop': '10px'}
        return fig, table_display, table_data.to_dict('records')
    if selected_plot == "library_strategy":
        return get_library_strategy_plot(data_overview)

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