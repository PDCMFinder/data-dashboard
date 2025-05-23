from src.assets.resources import reactive_categories
from plotly_express import bar, histogram


def get_bar_chart(models):
    color_code = {"PDX": "#6e9eeb", "Organoid": "#8f7cc3", "Cell Line": "#94c37e", "Other": "#ea921b"}
    fig = bar(models, x='Release', y='Model Count', color='Model Type', hover_data=['Total Models'], color_discrete_map=color_code)
    fig.update_layout(
        title=dict(text="Model Distribution per Data Release", yref='container')
    )
    return fig

def get_ss_bar_chart(models, cat):
    fig = bar(models, x='tag', y=cat, hover_data=[cat])
    fig.update_layout(
        title=dict(text="Summary statistics for a data type per Data Release", yref='container')
    )
    return fig

def get_reactive_bar_plot(data, column, gc):
    color_code = {"PDX": "#6e9eeb", "Organoid": "#8f7cc3", "Cell Line": "#94c37e", "Other": "#ea921b"}
    if gc is None or column == gc:
        fig = bar(data, x=column.lower(), y='count', color_discrete_map=color_code)
    else:
        total = data.groupby(column.lower()).sum(numeric_only=False)['count'].to_dict()
        data['Total'] = [total[r] for r in data[column.lower()]]
        fig = bar(data, x=column.lower(), y='count', color=gc, hover_name=gc, hover_data='Total', color_discrete_map=color_code)
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        fig.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})

        for trace in fig.data:
            trace.update(showlegend=False)
    if len(data[column]) > 15:
        fig.update_layout(
            xaxis=dict(
                tickfont=dict(size=9)
            ),
        )
    fig.update_layout(
        title=dict(text=f"Model counts for attribute {get_key_from_value(reactive_categories, column).title()}",
                   yref="container"),
    )
    return fig


def get_key_from_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None

def get_country_bar_plot(df):
    fig = bar(df, x='country', y='provider_count')
    fig.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})
    return fig


def get_molecular_model_type_plot(data):
    color_code = {"PDX": "#6e9eeb", "Organoid": "#8f7cc3", "Cell Line": "#94c37e", "Other": "#ea921b"}

    fig = bar(data, x='molecular_characterisation_type', y='count', color='model_type', hover_name='model_type',
              hover_data='total', color_discrete_map=color_code)
    fig.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})
    return fig

def get_metadata_score_plot(data, model_type):
    color_code = {"pdx": "#6e9eeb", "organoid": "#8f7cc3", "cell line": "#94c37e", "Other": "#ea921b"}
    fig = histogram(data, x='scores', color_discrete_sequence=[color_code[model_type]])
    return fig