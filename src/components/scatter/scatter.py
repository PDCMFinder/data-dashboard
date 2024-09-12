from src.components.resources import cancer_system, diagnosis_to_cancer, primary_site_mapping
import numpy as np
from pandas import DataFrame
from plotly_express import scatter


def get_scatter_plot(data):
    data['diagnosis'] = [diagnosis_to_cancer[d].title() if d in diagnosis_to_cancer else 'Not provided' for d in
                         data['diagnosis'].str.lower()]
    data['diagnosis'] = data['diagnosis'].str.replace(' Not Otherwise Specified', '')
    data = data.merge(cancer_system, left_on='diagnosis', right_on='histology', how='left')
    data['cancer_system'] = data.fillna('').apply(lambda row: primary_site_mapping[row['primary_site']] if row['cancer_system'] == '' else row['cancer_system'], axis=1)
    data['cancer_system'] = data['cancer_system'].str.lower().replace('not provided', 'Unclassified')
    data['cancer_system'] = data['cancer_system'].str.title()
    data = data[data['cancer_system'] != "Unclassified"]
    data = data.groupby('cancer_system').size().reset_index(name='Count')
    data['percent'] = round(data['Count'] / data['Count'].sum(), 1)
    centers = generate_circle_centers(data['percent'].to_list())
    data['x'] = centers.iloc[:, 0]
    data['y'] = centers.iloc[:, 1]
    fig = scatter(
            data,
            x='x',
            y='y',
            hover_data=['cancer_system', 'Count'],
            size='percent',
            color='cancer_system',
        ).update_layout(
            paper_bgcolor='rgba(255,255,255,0.8)',  # Set background color
            plot_bgcolor='rgba(255,255,255,0.8)',   # Set plot area background color
            margin=dict(l=20, r=20, t=30, b=20),     # Adjust margins
            xaxis=dict(showgrid=True, zeroline=False, showticklabels=False),  # Hide x-axis gridlines
            yaxis=dict(showgrid=True, zeroline=False, showticklabels=False),  # Hide y-axis gridlines
    )
    fig.update_layout(showlegend=False)
    #fig.update_traces(mode='markers', marker=dict(sizemode='area', sizeref=sizeref, line_width=2))


    return fig


def generate_circle_centers(side_lengths):
    total_squares = len(side_lengths)
    num_rows = int(np.ceil(np.sqrt(total_squares)))

    # Determine the size of the larger square to contain all smaller squares
    max_side_length = max(side_lengths)
    size_of_larger_square = num_rows * (max_side_length + 1)  # Add 1 for spacing

    # Initialize list to store square centers
    centers = []

    # Iterate over rows and columns to compute centers
    for i in range(num_rows):
        for j in range(num_rows):
            idx = i * num_rows + j
            if idx < total_squares:
                side_length = side_lengths[idx]
                x = i * (max_side_length + 1)
                y = j * (max_side_length + 1)
                center = (x + side_length / 2, y + side_length / 2)
                centers.append(center)
    return DataFrame(np.array(centers))




