from pandas import DataFrame, read_csv
from src.backend.pie_chart import get_dto_dount, get_dto_radial
from src.backend.venn import get_dt_venn
from src.backend.bar_chart import get_bar_chart
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
        table_display = {'display': 'block'}
        return fig, table_display, table_data.to_dict('records')

def bar_chart():
    return get_bar_chart()
