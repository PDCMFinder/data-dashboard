from pandas import DataFrame, ExcelWriter, read_json
from src.backend.venn_to_plotly import venn_to_plotly
from dash.dcc import send_file
from venn import venn
import io
import matplotlib.pyplot as plt
import base64

def get_dt_venn(filtered_data, plot_type):
    filtered_data = filtered_data.fillna('').groupby('molecular_characterisation_type')['model_id'].apply(set)
    set1, set2, set3 = process_sets(filtered_data['mutation']), process_sets(filtered_data['expression']), process_sets(filtered_data['copy number alteration'])
    labels = ['mutation', 'expression', 'copy number alteration']
    fig = venn_to_plotly([set1, set2, set3], labels)
    fig.update_layout(
        title=dict(text="Model data type overlaps", automargin=True, yref='paper')
    )
    return fig

def get_venn_table(df, output, model):
    model['links'] = "https://www.cancermodels.org/data/models/"+model['provider']+"/"+model['model_id']
    cancer_system = read_json("https://www.cancermodels.org/api/search_index?select=external_model_id,cancer_system")
    model = model.merge(cancer_system, left_on='model_id', right_on='external_model_id', how='left')
    filtered = df.fillna('').groupby('molecular_characterisation_type')['model_id'].apply(set).reset_index()
    data_type_sets = {}
    for i, row in filtered.iterrows():
        data_type_sets[row['molecular_characterisation_type']] = process_sets(row['model_id'])
    m_e_c = sorted(list(data_type_sets['mutation'].intersection(data_type_sets['expression']).intersection(data_type_sets['copy number alteration'])))
    m_e_c_i = sorted(list(set(m_e_c).intersection(data_type_sets['immunemarker'])))
    m_e_c_d = sorted(list(set(m_e_c).intersection(data_type_sets['drug'])))
    m_e_c_t = sorted(list(set(m_e_c).intersection(data_type_sets['treatment'])))
    m_e_c_b = sorted(list(set(m_e_c).intersection(data_type_sets['biomarker'])))
    m_e_c_b_i = sorted(list(set(m_e_c_i).intersection(data_type_sets['biomarker'])))
    t_d = sorted(list(set(data_type_sets['treatment']).intersection(data_type_sets['drug'])))
    m_e_c_t_d = sorted(list(set(m_e_c_t).intersection(t_d)))

    cols = ['mut_exp_cna', 'mut_exp_cna_immune', 'mut_exp_cna_drug', 'mut_exp_cna_treatment', 'mut_exp_cna_bio', 'mut_exp_cna_bio_immune', 'treatment_drug_dosing', 'mut_cna_exp_treatment_dosing']
    out_df = DataFrame([[m_e_c, m_e_c_i, m_e_c_d, m_e_c_t, m_e_c_b, m_e_c_b_i, t_d, m_e_c_t_d]], columns=cols)
    #output = io.BytesIO()
    # Create an Excel writer object and write the DataFrame to it
    writer = ExcelWriter(output)
    for index, row in out_df.transpose().reset_index().iterrows():
        row_df = DataFrame()
        row_df['model_id'] = row[0]
        row_df = row_df.merge(model, on='model_id', how='left')
        #row_df['provider'] = [df[df['model_id'] == m].reset_index(drop=True)['provider'][0] for m in row_df['model_id']]
        # age, diagnosis, ethnicity, model type, sex, tumor type
        row_df.to_excel(writer, sheet_name=f'{row["index"]}', index=False)
    # Save the Excel file to the bytes buffer
    writer.close()
    # Encode the bytes buffer to base64
    return send_file(output)

def get_dt_venn4(df):
    data_dict = df.groupby('molecular_characterisation_type')['model_id'].apply(set).to_dict()
    set1, set2, set3 = process_sets(data_dict['mutation']), process_sets(data_dict['expression']), process_sets(
        data_dict['copy number alteration'])
    data_dict['mutation_expression_cna'] = sorted(list(set1 & set2 & set3))
    if 'immunemarker' not in data_dict.keys():
        data_dict['immunemarker'] = set()
    data_subset_dict = dict(
        (k, process_sets(data_dict[k])) for k in ('mutation_expression_cna', 'drug', 'treatment', 'immunemarker'))
    plt.figure(figsize=(12, 12))
    buf = io.BytesIO()
    venn(data_subset_dict, figsize=(12,12), fontsize=20, legend_loc="upper left")
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return {
        'data': [],
        'layout': {
            'images': [{
                'source': "data:image/png;base64,{}".format(img_base64),
                'xref': 'paper',
                'yref': 'paper',
                'x': 0.5,
                'y': 0.5,
                'sizex': 1.8,
                'sizey': 1.8,
                'xanchor': 'center',
                'yanchor': 'middle'
            }],
            'xaxis': {'visible': False},
            'yaxis': {'visible': False}
        }
    }

def process_sets(s):
    s = set(s)
    s = {item for item in s if item != ''}
    return s