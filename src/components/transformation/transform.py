from pandas import read_csv, DataFrame
from src.assets.resources import primary_site_mapping, diagnosis_to_cancer_system

cache = {}

def load_data(release, score=None):
    if release in cache and score is None:
        return cache[release]
    if score is not None:
        metadata_scores = f"src/assets/metadata-scores-all-release.csv"
        metadata_scores = read_input_file(metadata_scores, ['model_id', 'provider', 'model_type',
                                                            release.replace('_', '_v').replace('DR', 'PDCM_DR')])
        return {'metadata_scores': metadata_scores}
    country = f"src/assets/country/provider_country_{release.replace('_', '_v')}.csv"
    country = read_csv(country)
    samples = f"src/assets/sample/{release.replace('_', '_v')}.csv"
    samples = read_input_file(samples)
    total_model = f"src/assets/model/total_models_{release.replace('_', '_v')}.csv"
    total_model = read_input_file(total_model)
    data = {'total': total_model, 'samples': samples, 'country': country, }
    cache[release] = data
    return data


def read_input_file(fname, cols=list()):
    if len(cols)>0:
        data = read_csv(fname, usecols=cols)
    else:
        data = read_csv(fname)
    return process_data_df(data)

def process_data_df(data: DataFrame) -> DataFrame:
    columns = data.columns
    if 'mt' in columns:
        data['model_type'] = data['mt']
        data.drop(['mt'], axis=1, inplace=True)
    if 'model_type' in columns:
        data.loc[:, 'model_type'] = ['Organoid' if str(t).lower().__contains__('organoid') else t for t in
                                     data['model_type']]
        data.loc[:, 'model_type'] = [
            'Cell Line' if str(t).lower().__contains__('cell') or str(t).lower().__contains__('pdc') or str(
                t).lower().__contains__('2d') or str(t).lower().__contains__('2-d') else t for t in data['model_type']]
        data.loc[:, 'model_type'] = [
            'Other' if str(t).lower().__contains__('other') or str(t).lower().__contains__('mixed') else t for t in
            data['model_type']]
    if 'diagnosis' in columns:
#        data['diagnosis'] = [diagnosis_to_cancer[d].title() if d in diagnosis_to_cancer else 'Not provided' for d in
#                             data['diagnosis'].str.lower()]
        data['diagnosis'] = [diagnosis_to_cancer_system[d] if d in diagnosis_to_cancer_system.keys() else 'Not provided' for d in
                                                  data['diagnosis'].str.lower()]
        data['diagnosis'] = data['diagnosis'].str.replace('Not provided', 'Unclassified')
    if 'primary_site' in columns:
        data['primary_site'] = data['primary_site'].str.title()
        data['primary_site'] = [next((f for f in primary_site_mapping if ps in primary_site_mapping[f]), 'Unmapped')  for ps in data['primary_site']]
        '''
        for j, r in data.iterrows():
            ps = r['primary_site']
            row = 'Unmapped'
            for i, f in enumerate(primary_site_mapping):
                if ps in primary_site_mapping[f]:
                    row = f
                    break
            data.loc[j, 'primary_site'] = row
        '''

    if 'tumour_type' in columns:
        data['tumour_type'] = [t.replace('Not Collected', 'Not provided').replace('Not Provided', 'Not provided') for t
                               in data['tumour_type'].fillna('Not provided').str.title()]
    if 'age_in_years_at_collection' in columns:
        data['age_in_years_at_collection'] = data['age_in_years_at_collection'].str.replace('--', 'Not provided')
    if 'sex' in columns:
        data['sex'] = data['sex'].str.title().replace('Not Provided', 'Not provided').replace('Not Collected',
                                                                                          'Not provided')
    if 'ethnicity' in columns:
        data['ethnicity'] = data['ethnicity'].str.title().replace('Not Provided', 'Not provided').replace('Not Collected',
                                                                                                      'Not provided')
    if 'publications' in columns:
        data['publications'] = data['publications'].fillna('No')
        data['publications'] = ['Yes' if str(p).__contains__('PMID') else 'No' for p in data['publications']]
    if 'age_in_years_at_collection' in columns:
        data['age_in_years_at_collection'] = data['age_in_years_at_collection'].str.replace('0-1', '1')
        data['age_in_years_at_collection'] = [
            'Younger than 21' if not str(a).lower().__contains__('not') and float(
                a) < 21 else 'Not provided' if str(
                a).lower().__contains__('not') else 'Older than 21' for a in data['age_in_years_at_collection']]
    return data