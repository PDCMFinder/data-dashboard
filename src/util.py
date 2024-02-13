from pandas import DataFrame, read_csv
from src.backend.pie_chart import get_model_type_donut, get_dto_radial, get_library_strategy_plot
from src.backend.venn import get_dt_venn
from src.backend.scatter import get_scatter_plot
from src.backend.bar_chart import get_bar_chart, get_reactive_bar_plot
from src.resources import input_file, total_models

data = DataFrame([[0, 0], [1, 1]], columns=['Type', 'Model'])


def custom_plots(selected_category, selected_plot):
    file = input_file[selected_category]
    data_overview = read_csv(file)
    if selected_plot == 'dto_donut':
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
    data = read_csv(file)
    return get_scatter_plot(data)

def model_type_pie(category):
    file = total_models[category]
    data = read_csv(file)
    return get_model_type_donut(data)

def reactive_bar_plot(release, category, gc):
    file = total_models[release]
    data = read_csv(file)
    return get_reactive_bar_plot(data, category, gc)