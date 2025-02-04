from src.components.bar.bar_chart import get_bar_chart
from src.components.DB.db import query_db
from src.components.line.line_plot import summary_line_plot

def bar_chart(engine):
    query = f"SELECT model_id, provider, model_type, release_label FROM total_models"
    models = query_db(engine, query).drop_duplicates(subset=['model_id', 'release_label']).groupby(
        ['release_label', 'model_type']).count()['model_id'].reset_index().rename(
        {'model_id': 'Model Count', 'release_label': 'Release', 'model_type': 'Model Type'}, axis=1)
    total = models.groupby('Release').sum(numeric_only=False)['Model Count'].to_dict()
    models['Total Models'] = [total[r] for r in models['Release']]
    return get_bar_chart(models)


def generate_summary_stats(engine):
    query = f"SELECT * FROM phenomics"
    return query_db(engine, query)

def generate_ss_bar_plot(df, cat):
    df = df.sort_values(by=['date']).reset_index(drop=True)
    return summary_line_plot(df, cat)