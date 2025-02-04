from src.components.bar.bar_chart import get_metadata_score_plot
from pandas import read_csv

def generate_metadata_score_bar_plot(release, model_type):
    data = get_ms_table(['model_id', 'provider', 'model_type', release.replace('_', '_v').replace('DR', 'PDCM_DR')])
    data['model_type'] = data['model_type'].str.lower()
    data = data[data['model_type'] == model_type]
    data = data.rename([{c: 'scores'} for c in data.columns if c.__contains__('PDCM')][0], axis=1)
    return get_metadata_score_plot(data, model_type)


def get_ms_table(cols=None):
    if cols is None:
        return read_csv('src/assets/metadata-scores-all-release.csv')
    return read_csv('src/assets/metadata-scores-all-release.csv', usecols=cols)