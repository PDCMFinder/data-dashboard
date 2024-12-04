from src.components.table.tables import get_ms_table
from plotly.graph_objects import Figure, Scatter
def plot_line_plot_ms(selected_rows):
        figure = Figure()
        df = get_ms_table()
        if selected_rows:
            for i in selected_rows:
                row = df.iloc[i]
                x_labs = [r for r in row.index if r.__contains__('PDCM')]
                figure.add_trace(Scatter(
                    x=x_labs,
                    y=[row[r] for r in x_labs],
                    mode='lines+markers',
                    name= f"{row['provider']}: {row['model_id']}"
                ))

        # Update the layout
        figure.update_layout(
            title='Line Plot of Model scores over releases',
            xaxis_title='Release',
            yaxis_title='Score'
        )
        return figure