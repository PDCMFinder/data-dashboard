from plotly_express import box


def plot_boxplot(df):
    if df.shape[0] == 0:
        return box()
    df['log transformed fpkm'] = df['rnaseq_fpkm_log']
    fig = box(df, x='cancer_system', y='log transformed fpkm')
    return fig