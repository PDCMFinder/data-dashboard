from pandas import DataFrame
from src.backend.venn_to_plotly import venn_to_plotly


def get_dt_venn(filtered_data):
    filtered_data = filtered_data.fillna('').groupby('molecular_characterisation_type')['model_id'].apply(set)
    set1, set2, set3 = set(filtered_data['mutation']), set(filtered_data['expression']), set(filtered_data['copy number alteration'])
    set1, set2, set3 = {item for item in set1 if item != ''}, {item for item in set2 if item != ''}, {item for item in set3 if item != ''}
    labels = ['mutation', 'expression', 'copy number alteration']
    fig = venn_to_plotly([set1, set2, set3], labels)
    intersection = sorted(list(set1 & set2 & set3))
    set1_and_set2 = sorted(list(set1 & set2))
    set1_and_set3 = sorted(list(set1 & set3))
    set2_and_set3 = sorted(list(set2 & set3))
    operations = ['All three (Intersection)', 'Mutation and Expression', 'Mutation and Copy Number Alteration', 'Expression and Copy Number Alteration']
    values = [intersection, set1_and_set2, set1_and_set3, set2_and_set3]
    venn_df = DataFrame({'Type': operations, 'Model': [str(v) for v in values]})
    return fig, venn_df