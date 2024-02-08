from pandas import DataFrame, read_csv
from src.backend.pie_chart import get_dto_dount
from src.backend.venn import get_dt_venn
from src.backend.bar_chart import get_bar_chart


data = DataFrame([[0, 0], [1, 1]], columns=['Type', 'Model'])


def custom_plots(selected_category, selected_plot):
    data_overview = read_csv(selected_category)
    if selected_plot == 'dto_donut':
        fig = get_dto_dount(data_overview)
        table_data = data
        table_display = {'display': 'none'}
    if selected_plot == 'dt_venn':
        fig, table_data = get_dt_venn(data_overview)
        table_display = {'display': 'block'}
    return fig, table_display, table_data.to_dict('records')

def bar_chart():
    return get_bar_chart()
