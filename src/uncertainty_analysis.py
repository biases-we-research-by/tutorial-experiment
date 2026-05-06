import pandas as pd
from typing import Dict, Set,Tuple
import yaml
from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np


def find_overlaps(names:Tuple[str],paths:Tuple[str],decile:int=9) -> Dict[str,Set[str]]:


    df1 = pd.read_csv(paths[0])
    df2 = pd.read_csv(paths[1])

    df1 = df1[df1.decile>=decile]
    df2 = df2[df2.decile>=decile]

    df1 = set(df1.entity)
    df2 = set(df2.entity)
    

    overlap_ab = df1.intersection(df2)
    
    return {'model_a':names[0],
            'model_b':names[1],
            'ratio_overlap': len(overlap_ab)/len(df1),
    'overlapping_entities': overlap_ab,
    }


def socio_demographics(trait:str,entities:set):
    a = pd.read_csv(f"wd_entities/{trait}.csv")
    #a = a[(a[trait]=='Q6581097') | (a[trait]=='Q6581072')]
    a = a[a[trait]!='{}']
    b = pd.DataFrame(list(entities), columns=['entity'])

    c = a.merge(b)

    return {'general_distribution': a[trait].value_counts(normalize=True).head(5), 
            'uncertainty_distribution': c[trait].value_counts(normalize=True).head(5)
    }



def plot_distributions(data: Dict,title:str):
    """
    Plots general_distribution and uncertainty_distribution side by side.

    Args:
        data: dict with keys 'general_distribution' and 'uncertainty_distribution',
              each a pd.Series of proportions indexed by generation name.
    """
    general = data["general_distribution"]
    uncertainty = data["uncertainty_distribution"]

    # Align on a common index (union of both)
    all_gens = general.index.union(uncertainty.index)
    general = general.reindex(all_gens, fill_value=0)
    uncertainty = uncertainty.reindex(all_gens, fill_value=0)

    # Sort by general distribution descending
    order = general.sort_values(ascending=False).index
    general = general[order]
    uncertainty = uncertainty[order]

    x = np.arange(len(order))
    width = 0.38

    fig, ax = plt.subplots(figsize=(10, 5))

    bars1 = ax.bar(x - width / 2, general * 100, width, label="General", color="#378ADD", alpha=0.9)
    bars2 = ax.bar(x + width / 2, uncertainty * 100, width, label="Uncertainty", color="#D4537E", alpha=0.85)

    ax.bar_label(bars1, fmt="%.1f%%", padding=3, fontsize=9, color="#185FA5")
    ax.bar_label(bars2, fmt="%.1f%%", padding=3, fontsize=9, color="#993556")

    ax.set_xticks(x)
    ax.set_xticklabels(order, rotation=15, ha="right", fontsize=10)
    ax.set_ylabel("Proportion (%)")
    ax.set_ylim(0, max(general.max(), uncertainty.max()) * 130)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    ax.grid(axis="y", color="lightgray", linewidth=0.5)
    ax.set_title(title, fontsize=12, pad=15)

    plt.tight_layout()
    plt.show()


cnf = yaml.safe_load(open('config.yml','r'))


models = cnf['uncertainty']['models']

mymodels = [x for x in models]
mymodels = list(combinations(models, 2))

for model_a, model_b in mymodels:
    print(models[model_a],models[model_b])
    print(f"Comparing {model_a} and {model_b}")
    overlaps_ab = find_overlaps(names=(model_a, model_b), paths=(models[model_a], models[model_b]), decile=9)   

    bias = socio_demographics(trait=cnf['uncertainty']['axes']['wikidata']['P27'], entities=overlaps_ab['overlapping_entities'])
    
    plot_distributions(bias,title=f"Comparing {model_a} and {model_b}")