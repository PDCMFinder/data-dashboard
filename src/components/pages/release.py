from pandas import DataFrame, concat
from src.components.DB.db import query_db
from src.components.overlap.overlap_plot import overlap_diagram
from src.components.pie.pie_chart import get_model_type_donut
from src.components.bar.bar_chart import get_reactive_bar_plot, get_country_bar_plot, get_molecular_model_type_plot
from src.components.pie.pie_chart import get_dto_radial, get_library_strategy_plot
from src.components.venn.venns import get_dt_venn, get_dt_venn4, get_venn_table, process_sets


def generate_overlap_diagram(engine, release, width):
    query = f"SELECT model_id, provider, molecular_characterisation_type FROM SAMPLES WHERE dr='{release}';"
    samples = query_db(engine, query)
    query2 = f"SELECT model_id, publication, provider FROM total_models WHERE dr='{release}';"
    publication_counts = query_db(engine, query2)
    publication_counts['publication'] = [0 if p == 'No' else 1 for p in publication_counts['publication']]
    result = (
        samples.groupby(["model_id", "provider", "molecular_characterisation_type"])
        .size()
        .unstack(fill_value=0)  # Fill missing values with 0
        .applymap(lambda x: 1 if x > 0 else 0)  # Convert to 1 if data exists
    )
    result = result.reset_index()
    # result = result.merge(publication_counts, on=['model_id', 'provider'], how='right')
    columns = result.columns[2:]
    for c in columns:
        result[c] = result[c].fillna(0).astype(int)
    return overlap_diagram(result[columns], width)

def model_type_pie(engine, release, type):
    query = f"SELECT model_id, provider, model_type FROM TOTAL_MODELS WHERE dr='{release}';"
    models = query_db(engine, query)
    if type == 'plot':
        return get_model_type_donut(models.drop_duplicates(['model_id']))
    else:
        return models.drop_duplicates(['model_id']).groupby('model_type').count()['provider'].reset_index()

def reactive_bar_plot(engine, release, category, gc, plot_type):
    query = f"SELECT model_id, provider, model_type FROM TOTAL_MODELS WHERE dr='{release}';"
    models = query_db(engine, query)

    query2 = f"SELECT * FROM COUNTRY WHERE dr='{release}';"
    country = query_db(engine, query2)

    models = models.merge(country[['provider', 'country']], on='provider', how='left')
    groupby_columns = [category]
    if gc is not None and category != gc:
        groupby_columns.append(gc)
    models = models.groupby(groupby_columns).size().reset_index(name='Count').sort_values(by=category)
    models = models[models[category] != "Not provided"]
    if plot_type == 'table':
        return models
    return get_reactive_bar_plot(models, category, gc)

def generate_country_plot(engine, release, plot_type):
    query = f"SELECT * FROM COUNTRY WHERE dr='{release}';"
    country = query_db(engine, query)[['country', 'provider']]
    df = country.groupby('country')['provider'].apply(list).reset_index(name='provider')
    df['provider'] = df['provider'].astype(str)
    if plot_type == 'table':
        return country.groupby('country').count()['provider'].reset_index()
    return get_country_bar_plot(country), df.to_dict('records')

def molecular_model_type_plot(engine, release, plot_type):
    query = f"SELECT model_id, molecular_characterisation_type FROM SAMPLES WHERE dr='{release}';"
    samples = query_db(engine, query)

    query2 = f"SELECT model_id, model_type FROM TOTAL_MODELS WHERE dr='{release}';"
    models = query_db(engine, query2)

    temp = samples.drop_duplicates().merge(models, on='model_id', how='left')
    data = temp.groupby(['molecular_characterisation_type', 'model_type']).size().reset_index(name='Count')
    total = data.groupby('molecular_characterisation_type').sum(numeric_only=False)['Count'].to_dict()
    data['Total'] = [total[r] for r in data['molecular_characterisation_type']]
    if plot_type == 'table':
        return data
    return get_molecular_model_type_plot(data)

def dto_donut(engine, release, export_type='plot'):
    query = f"SELECT model_id, molecular_characterisation_type FROM SAMPLES WHERE dr='{release}';"
    samples = query_db(engine, query)

    query2 = f"SELECT model_id, publication FROM total_models WHERE dr='{release}';"
    publication_counts = query_db(engine, query2)
    tm = publication_counts.shape[0]
    publication_counts = publication_counts.groupby('publication').count().reset_index().iloc[1][1]

    pie_table = samples.drop_duplicates(['model_id', 'molecular_characterisation_type']).groupby(
        'molecular_characterisation_type').count().sort_index()['model_id'].sort_values().to_frame()
    pie_table = concat(
        [pie_table, DataFrame({'model_id': publication_counts}, index=['publication'])]).sort_values(
        'model_id').reset_index()
    if export_type == 'table':
        return pie_table.sort_index().reset_index()
    fig = get_dto_radial(pie_table, int(tm))
    return fig

def library_strategy(engine, release, export_type='plot'):
    query = f"SELECT model_id, molecular_characterisation_type, library_strategy FROM SAMPLES WHERE dr='{release}';"
    samples = query_db(engine, query)

    samples['library_strategy'] = samples['library_strategy'].fillna('Not Provided').astype(str).str.replace('mRNA NGS',
                                                                                                             'RNA-Seq').replace(
        'WXS', 'WES').replace('microarray', 'Microarray')
    samples['library_strategy'] = ['Targeted' if str(t).lower().__contains__('target') else t for t in
                                   samples['library_strategy']]
    if export_type == 'table':
        return samples.groupby(['molecular_characterisation_type', 'library_strategy']).count()[
            'model_id'].reset_index()
    return get_library_strategy_plot(samples)

def dt_venn(engine, release, plot_type, export_type='plot'):
    query = f"SELECT model_id, sample_id, provider, molecular_characterisation_type FROM SAMPLES WHERE dr='{release}';"
    samples = query_db(engine, query)
    plot_type = plot_type.split('_')[-1]

    query2 = f"SELECT model_id, provider, model_type FROM TOTAL_MODELS WHERE dr='{release}';"
    models = query_db(engine, query2)

    if plot_type != 'Total' and plot_type != 'venn':
        models = models[models['model_type'] == plot_type]
        samples = samples[['sample_id', 'provider', 'molecular_characterisation_type', 'model_id']].merge(models, on=[
            'model_id', 'provider'], how='inner')
    if export_type == 'table':
        return get_venn_table(samples, f"assets/exports/{release}_mol_data_model_list.xlsx", models)
    return get_dt_venn(samples, export_type)

def venn4_plots(engine, release, plot_type):
    query = f"SELECT model_id, molecular_characterisation_type FROM SAMPLES WHERE dr='{release}';"
    samples = query_db(engine, query)

    data_dict = samples.groupby('molecular_characterisation_type')['model_id'].apply(set).to_dict()
    set1, set2, set3 = process_sets(data_dict['mutation']), process_sets(data_dict['expression']), process_sets(
        data_dict['copy number alteration'])
    data_dict['mutation_expression_cna'] = sorted(list(set1 & set2 & set3))
    if plot_type == 'biomarker':
        if 'biomarker' not in data_dict.keys():
            data_dict['biomarker'] = set()
        data_type_list = ('mutation_expression_cna', 'drug', 'treatment', 'biomarker')
    else:
        if 'immunemarker' not in data_dict.keys():
            data_dict['immunemarker'] = set()
        data_type_list = ('mutation_expression_cna', 'drug', 'treatment', 'immunemarker')

    data_subset_dict = dict((k, process_sets(data_dict[k])) for k in data_type_list)
    return get_dt_venn4(data_subset_dict)

