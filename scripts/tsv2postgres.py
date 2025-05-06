import pandas as pd
from requests import get
from pandas import read_csv, DataFrame
from src.assets.resources import primary_site_mapping, diagnosis_to_cancer_system, gene_list
from os import listdir
from os.path import isfile, join, isdir
from tqdm import tqdm
import json
import psycopg2
import os

home = '/Users/tushar/CancerModels/pdxfinder-data/data/UPDOG'

def test_connection():
    # Load environment variables
    DB_HOST = os.getenv("DB_HOST", "pdcm-data-dashboard-db-service.pdcm-data-dashboard.svc.cluster.local")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "data-dashboard")
    DB_USER = os.getenv("DB_USER", "admin")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "cGFzc3dvcmQ=")

    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Connected to PostgreSQL successfully!")
    except Exception as e:
        print("Error connecting to PostgreSQL:", e)


cache = {}
labels = {'DR_6.7': 'Data release 6.7', 'DR_6.6': 'Data release 6.6', 'DR_6.5': 'Data release 6.5', 'DR_6.4': 'Data release 6.4', 'DR_6.3': 'Data release 6.3', 'DR_6.2': 'Data release 6.2', 'DR_6.1': 'Data release 6.1', 'DR_6.0': 'Data release 6.0',
          'DR_5.3': 'Data release 5.3', 'DR_5.2': 'Data release 5.2', 'DR_5.1': 'Data release 5.1',
          'DR_4.0': 'Data release 4.0',
          'DR_3.1': 'Data release 3.1', 'DR_3.0': 'Data release 3.0',
          'DR_2.1': 'Data release 2.1', 'DR_2.0': 'Data release 2.0',
          'DR_1.0': 'Data release 1.0'}

def load_data(release, score=None):
    if release in cache and score is None:
        return cache[release]
    if score is not None:
        metadata_scores = f"src/assets/metadata-scores-all-release.csv"
        metadata_scores = read_input_file(metadata_scores, ['model_id', 'provider', 'model_type',
                                                            release.replace('_', '_v').replace('DR', 'PDCM_DR')])
        return {'metadata_scores': metadata_scores}
    country = f"../src/assets/country/provider_country_{release.replace('_', '_v')}.csv"
    country = read_csv(country)
    samples = f"../src/assets/sample/{release.replace('_', '_v')}.csv"
    samples = read_input_file(samples)
    total_model = f"../src/assets/model/total_models_{release.replace('_', '_v')}.csv"
    total_model = read_input_file(total_model)
    country['release_label'] = labels[release]
    country['DR'] = release
    samples['release_label'] = labels[release]
    samples['DR'] = release
    total_model['release_label'] = labels[release]
    total_model['DR'] = release
    total_model = total_model[~total_model['model_id'].isna()]
    data = {'total': total_model.drop_duplicates(['model_id', 'provider', 'DR']), 'samples': samples, 'country': country}
    cache[release] = data
    return data

def generate_summary_stats():
    table = DataFrame()
    for f in get("https://gitlab.ebi.ac.uk/api/v4/projects/1629/releases?private_token=glpat-gbQzKFxHTWyp_jZhP5gE").json():
        if f['tag_name'].replace('PDCM_', '').replace('v', '') in labels.keys():
            df = read_csv(f"../src/assets/phenomic/phenomics_data_points_{f['tag_name'].replace('PDCM_', '')}.csv").groupby('release').sum(numeric_only=False).reset_index()
            total_model = f"../src/assets/model/total_models_{f['tag_name'].replace('PDCM_DR_v', 'DR_').replace('_', '_v')}.csv"
            data = read_csv(total_model, usecols=['model_id', 'model_type', 'mt'])
            data['model_type'] = data['mt']
            data = data.groupby('model_type').count()['model_id'].reset_index()
            df['model_type_cell_line'] = data[data['model_type'].str.contains('Cell')].reset_index(drop=True)['model_id'][0]
            df['model_type_organoid'] = data[data['model_type'].str.contains('Organoid')].reset_index(drop=True)['model_id'][0]
            df['model_type_pdx'] = data[data['model_type'].str.contains('PDX')].reset_index(drop=True)['model_id'][0]
            df['model_type_other'] = data[data['model_type'].str.contains('Other')].reset_index(drop=True)['model_id'][0]
            df['model_type_total'] = data['model_id'].sum()

            df['date'] = f['released_at'].split('T')[0]
            df['tag'] = labels[f['tag_name'].replace('PDCM_', '').replace('v', '')]
            df['links'] = f"[View](/data-release?dropdown-category={f['tag_name'].replace('PDCM_', '').replace('v', '')})"
            table = pd.concat([table, df]).reset_index(drop=True)
    return table


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

def generate_files_for_db(releases):
    total_df = pd.DataFrame()
    samples_df = pd.DataFrame()
    country_df = pd.DataFrame()
    for release in releases:
        data = load_data(release)
        total_df = pd.concat([total_df, data['total']])
        samples_df = pd.concat([samples_df, data['samples']])
        country_df = pd.concat([country_df, data['country']])
    samples_df = samples_df.fillna('')
    samples_df = samples_df[samples_df['model_id'] != '']
    samples_df = samples_df[~samples_df['model_id'].str.contains('free')]
    samples_df = samples_df[~samples_df['model_id'].str.contains('Unique')]
    samples_df = samples_df[~samples_df['model_id'].str.contains('desirable')]
    samples_df = samples_df[~samples_df['model_id'].str.contains('essential')]
    samples_df = samples_df.drop_duplicates(
        subset=['DR', 'provider', 'model_id', 'sample_id', 'molecular_characterisation_type'])
    summary_df = generate_summary_stats()
    total_df.to_csv('total_models_db.tsv', sep='\t', index=False)
    samples_df.to_csv('samples_db.tsv', sep='\t', index=False)
    country_df.to_csv('country_db.tsv', sep='\t', index=False)
    summary_df.to_csv('phenomics_db.tsv', sep='\t', index=False)


def read_metadata_without_fields(path):
    metadata = pd.read_csv(path, sep='\t', na_values="", low_memory=False, encoding='utf-8', encoding_errors='replace')
    if 'Field' in metadata.columns:
        metadata = metadata.loc[metadata.Field.astype(str).str.startswith('#') != True,].reset_index(drop=True)
        metadata = metadata.drop('Field', axis=1)
    return metadata


def read_metadata_with_fields(path, columns):
    metadata = pd.read_csv(path, usecols=columns,sep='\t', na_values="", low_memory=False, encoding='utf-8', encoding_errors='replace')
    return metadata

def get_dirs(path):
    return [f for f in listdir(path) if isdir(join(path, f))]


def get_files(path):
    return [join(path, f) for f in listdir(path) if isfile(join(path, f)) and f != '.DS_Store' and f.endswith('.tsv')]

def generate_data_visualisation_files():
    home = '/Users/tushar/CancerModels/pdxfinder-data/data/UPDOG'
    search_index = pd.read_json('https://www.cancermodels.org/api/search_index?select=data_source,external_model_id,cancer_system,model_type')
    #data_table = pd.read_json('https://www.cancermodels.org/api/data_overview_mutation_cohorts')[['model_id', 'sample_id', 'symbol','provider', 'type', 'cancer_system']]
    providers = sorted(get_dirs(home))
    mutation_df, expression_df = DataFrame(), DataFrame()
    mut_columns = ['sample_id', 'symbol','amino_acid_change', 'consequence', 'read_depth', 'chromosome', 'strand', 'seq_start_position', 'ref_allele', 'alt_allele']
    #exp_columns = ['sample_id', 'symbol', 'rnaseq_fpkm']
    for p in providers:
        if 'mut' in get_dirs(join(home, p)):
            mutation_df = merge_tsv_to_df(join(home, p, 'mut'), mut_columns, mutation_df, p)
        #if 'expression' in get_dirs(join(home, p)):
        #    expression_df = merge_tsv_to_df(join(home, p, 'expression'), exp_columns, expression_df, p)
    mutation_df.to_csv('raw_mutation_df.tsv', sep='\t', index=False)
    mutation_df = mutation_df.merge(search_index, left_on=['model_id', 'provider'], right_on=['external_model_id', 'data_source'], how='left')
    mutation_df.drop_duplicates(subset=['symbol', 'amino_acid_change', 'chromosome', 'seq_start_position', 'ref_allele', 'alt_allele', 'cancer_system']).to_csv('mutation_df.tsv', sep='\t', index=False)
    #expression_df.to_csv('expression_df.tsv', sep='\t', index=False)

def merge_tsv_to_df(path, columns, mut_df, provider):
    df = pd.DataFrame()
    files = get_mol_files(path)
    mms = read_metadata_without_fields(f"{home}/{provider}/{provider}_molecular_metadata-sample.tsv")[['model_id', 'sample_id']].drop_duplicates()
    for f in tqdm(files, path):
        try:
            temp = read_metadata_with_fields(f, columns)
            temp['provider'] = provider
            #temp = temp[temp['symbol'].isin(gene_list)]
            if 'ref_allele' in temp.columns or 'alt_allele' in temp.columns:
                temp['ref_allele'] = temp['ref_allele'].str.split(',').str[0]
                temp['alt_allele'] = temp['alt_allele'].str.split(',').str[0]
        except:
            print(f)
            exit(1)
        df = pd.concat([df, temp]).reset_index(drop=True)
    df = df.merge(mms, on='sample_id', how='left')
    mut_df = pd.concat([mut_df, df]).reset_index(drop=True)
    return mut_df

def flatten(xss):
    return [x for xs in xss for x in xs]

def get_mol_files(path):
    files = []
    if len(get_dirs(path)) > 0:
        for d in get_dirs(path):
            new_path = join(path, d)
            files.append(get_files(new_path))
        files = flatten(files)
    else:
        files = get_files(path)
    return files


def generate_mutation_plot_json(df):
    df = df.drop_duplicates(subset=['chromosome', 'seq_start_position', 'ref_allele', 'alt_allele', 'symbol'])
    annotations_dict = {}
    keys = ["name", "start", "length", "expression-level", "gene-type"],
    for chr in range(1, 25):
        if chr == 24:
            chr = 'Y'
        elif chr == 23:
            chr = 'X'
        temp = df[df['chromosome'] == str(chr)]
        for _, item in temp.iterrows():
            annotation_entry = [
                f'{item["symbol"]}, {item["consequence"]}, {item["ref_allele"]}/{item["alt_allele"]}',
                # name
                int(float(item["seq_start_position"])),  # start
                1,  # length (assuming a default of 1)
                1,  # int(item["read_depth"]),  # expression-level
                1,  # item["type"]  # gene-type (PDX, Organoid, etc.)
            ]
            if str(chr) not in annotations_dict:
                annotations_dict[str(chr)] = {"chr": str(chr), "annots": []}
            annotations_dict[str(chr)]["annots"].append(annotation_entry)
    annotations_list = list(annotations_dict.values())
    output_data = {
        "keys": keys[0],
        "annots": annotations_list
    }
    return output_data

def generate_mutation_plot_json_all_cancer():
    df = read_csv('mutation_df.tsv', sep='\t', low_memory=False, encoding='utf-8')
    cancer_systems = df['cancer_system'].unique()
    print(cancer_systems)
    for c in cancer_systems:
        t = generate_mutation_plot_json(df[df['cancer_system'] == c])
        with open(f'{c}.json', 'w') as f:
            json.dump(t, f)


if __name__ == "__main__":
    generate_data_visualisation_files()
    generate_mutation_plot_json_all_cancer()

    #generate_files_for_db(labels)
    #test_connection()
