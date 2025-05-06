from pandas.core.interchange.dataframe_protocol import DataFrame

from src.components.DB.db import query_db
from src.components.overlap.overlap_plot import overlap_diagram
from src.components.pie.pie_chart import get_model_type_donut
from src.components.bar.bar_chart import get_reactive_bar_plot, get_country_bar_plot, get_molecular_model_type_plot
from src.components.pie.pie_chart import get_dto_radial, get_library_strategy_plot
from src.components.venn.venns import get_dt_venn, get_dt_venn4


def generate_overlap_diagram(engine, release, width):
    query = f"select * from mv_model_overlap_diagram where dr='{release}';"
    df = query_db(engine, query)
    columns = df.columns[3:]
    df = df[columns]
    for c in columns:
        df[c] = df[c].fillna(0).astype(int)
    return overlap_diagram(df, width)

def model_type_pie(engine, release, type):
    query = f"SELECT model_type, COUNT(DISTINCT model_id) AS model_count FROM TOTAL_MODELS WHERE dr = '{release}' GROUP BY model_type;"
    models = query_db(engine, query).dropna(subset=['model_type'])

    if type == 'plot':
        return get_model_type_donut(models)
    else:
        return models

def reactive_bar_plot(engine, release, category, gc, plot_type):
    groupby_columns = [category]
    if gc is not None and category != gc:
        groupby_columns.append(gc)

    groupby_clause = ", ".join(groupby_columns)  # Create the GROUP BY clause
    if gc == 'country' or category == 'country':
        if gc == 'provider':
            select_clause = category
        elif category == 'provider':
            select_clause = gc
        elif gc == 'model_type' or category == 'model_type':
            if gc == 'model_type':
                select_clause = category
            else:
                select_clause = gc
        else:
            select_clause = groupby_clause

        query = (f"    WITH model_data AS (\n"
             f"        SELECT *\n"
             f"        FROM TOTAL_MODELS\n"
             f"        WHERE dr = '{release}'\n"
             f"    ),\n"
             f"    country_data AS (\n"
             f"        SELECT provider, country\n"
             f"        FROM COUNTRY\n"
             f"        WHERE dr = '{release}'\n"
             f"    ),\n"
             f"    merged_data AS (\n"
             f"        SELECT \n"
             f"            m.model_id, \n"
             f"            m.provider, \n"
             f"            m.model_type, {select_clause}\n"
             f"        FROM model_data m\n"
             f"        LEFT JOIN country_data c ON m.provider = c.provider\n"
             f"    )\n"
             f"    SELECT \n"
             f"        {groupby_clause}, \n"
             f"        COUNT(*) AS Count\n"
             f"    FROM merged_data\n"
             f"    WHERE {category} != 'Not provided'\n"
             f"    GROUP BY {groupby_clause}\n"
             f"    ORDER BY {category};\n")
    else:
        query = (f"    SELECT \n"
             f"        {groupby_clause}, \n"
             f"        COUNT(*) AS Count\n"
             f"    FROM TOTAL_MODELS\n"
             f"    WHERE {category} != 'Not provided' AND dr = '{release}'\n"
             f"    GROUP BY {groupby_clause}\n"
             f"    ORDER BY {category};\n")
    models = query_db(engine, query)
    if plot_type == 'table':
        return models
    return get_reactive_bar_plot(models, category, gc)

def generate_country_plot(engine, release, plot_type):
    query = f"SELECT * FROM mv_country_provider_summary WHERE dr = '{release}';"
    df = query_db(engine, query)
    print(df.head())
    if plot_type == 'table':
        return df
    return get_country_bar_plot(df[['country', 'provider_count']]), df[['country', 'provider']].to_dict('records')

def molecular_model_type_plot(engine, release, plot_type):
    query = f"select * from mv_sample_model_counts where release = '{release}';"
    data = query_db(engine, query)
    if plot_type == 'table':
        return data
    return get_molecular_model_type_plot(data)

def dto_donut(engine, release, export_type='plot'):
    query = f"select * from mv_molecular_publication_counts where release = '{release}';"
    pie_table = query_db(engine, query).fillna('')
    query2 = f"SELECT COUNT(DISTINCT model_id)  FROM total_models WHERE dr = '{release}';"
    tm = query_db(engine, query2).iloc[0,0]
    if export_type == 'table':
        return pie_table.sort_index().reset_index()
    fig = get_dto_radial(pie_table, int(tm))
    return fig

def library_strategy(engine, release, export_type='plot'):
    query = f"select * from mv_transformed_samples where release = '{release}';"
    df = query_db(engine, query)
    if export_type == 'table':
        return df
    return get_library_strategy_plot(df)

def dt_venn(engine, release, plot_type, export_type='plot'):
    table = plot_type.split('_')[-1].lower().replace(' ', '_')
    query = f"select * from mv_venn_plot_{table} where dr = '{release}';"
    df = query_db(engine, query).groupby("molecular_characterisation_type")["model_ids"].sum().to_dict()
    return get_dt_venn(df, export_type)

def venn4_plots(engine, release, plot_type):
    if plot_type == 'biomarker':
        table_name = 'mv_biomarker_data'
    else:
        table_name = 'mv_immune_marker_data'
    query = f"SELECT data_type, model_ids FROM {table_name} WHERE dr='{release}';"
    data = query_db(engine, query)
    for _, r in data.iterrows():
        data.iloc[_]['model_ids'] = process_sets(data.iloc[_]['model_ids'])
    data = dict(zip(data['data_type'], data['model_ids']))
    return get_dt_venn4(data)



def process_sets(s):
    s = set(s)
    s = {item for item in s if item != ''}
    return s
