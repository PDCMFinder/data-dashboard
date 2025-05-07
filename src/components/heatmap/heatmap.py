from plotly.express import imshow

def plot_heatmap(df):
    fig =  imshow(df.pivot(columns=['model_id', 'sample_id'], index='symbol', values='rnaseq_fpkm_log'),
                  labels=dict(x="Samples", y="Gene Symbol", color="Log transformed FPKM"))
    fig.update_xaxes(showticklabels=False)
    return fig