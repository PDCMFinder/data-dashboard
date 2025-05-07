from src.components.boxplot.boxplot import plot_boxplot
from src.components.heatmap.heatmap import plot_heatmap
from pandas import read_json
import json
from src.components.DB.db import query_db
from src.assets.resources import engine

def generate_expression_boxplot(cancer_system, gene_symbol, model_type):
    #query = f"symbol=eq.{gene_symbol}"

    if isinstance(cancer_system, list):
        cancer_system = ','.join(cancer_system)
        query = f"cancer_system=in.({cancer_system.replace(' ', '%20')})&symbol=eq.{gene_symbol}"
    else:
        query = f"cancer_system=eq.{cancer_system.replace(' ', '%20')}&symbol=eq.{gene_symbol}"
    if model_type != 'All':
        query = f"{query}&type=eq.{model_type.replace(' ', '%20')}"
    df = read_json(f"https://www.cancermodels.org/api/data_overview_expression_cohorts?{query}")
    return plot_boxplot(df)


def generate_expression_heatmap(cancer_system, gene_symbol, model_type):
    #query = f"symbol=eq.{gene_symbol}"

    if isinstance(gene_symbol, list):
        gene_symbol = ','.join(gene_symbol)
        query = f"cancer_system=eq.{cancer_system.replace(' ', '%20')}&symbol=in.({gene_symbol.replace(' ', '%20')})"
    else:
        query = f"cancer_system=eq.{cancer_system.replace(' ', '%20')}&symbol=eq.{gene_symbol.replace(' ', '%20')}"
    if model_type != 'All':
        query = f"{query}&type=eq.{model_type.replace(' ', '%20')}"
    df = read_json(f"https://www.cancermodels.org/api/data_overview_expression_cohorts?{query}")
    return plot_heatmap(df.drop_duplicates(subset=['model_id', 'sample_id', 'symbol']))

def generate_mutation_ideogram(cancer_system):
    """
    query = f"SELECT * from data_visualisation_mutation WHERE cancer_system='{cancer_system}' limit 1000000;"
    df = query_db(engine, query)
    df['chromosome'] = df['chromosome'].astype(int)
    annotations_dict = {}
    keys = ["name", "start", "length", "expression-level", "gene-type"],
    for chr in range(1,22):
        temp = df[df['chromosome'] == chr]
        for _, item in temp.iterrows():
            annotation_entry = [
                f'Gene: {item["symbol"]}, Mutation: {item["consequence"]}, ref/alt allele: {item["ref_allele"]}/{item["alt_allele"]}',  # name
                int(float(item["seq_start_position"])),  # start
                1,  # length (assuming a default of 1)
                1, #int(item["read_depth"]),  # expression-level
                1, #item["type"]  # gene-type (PDX, Organoid, etc.)
            ]
            if str(chr) not in annotations_dict:
                annotations_dict[str(chr)] = {"chr": str(chr), "annots": []}
            annotations_dict[str(chr)]["annots"].append(annotation_entry)
    annotations_list = list(annotations_dict.values())
    output_data = {
        "keys": keys[0],
        "annots": annotations_list
    }
    """
    with open(f"src/assets/mutation_json/{cancer_system}.json") as f:
        d = json.load(f)
    return d