from pandas import read_csv, DataFrame
from src.resources import diagnosis_to_cancer

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
        data['diagnosis'] = [diagnosis_to_cancer[d].title() if d in diagnosis_to_cancer else 'Not provided' for d in
                             data['diagnosis'].str.lower()]
    if 'primary_site' in columns:
        data['primary_site'] = data['primary_site'].str.title()
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
    return data