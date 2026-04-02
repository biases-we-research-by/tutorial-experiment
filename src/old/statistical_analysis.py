import os
import pandas as pd
import numpy as np
from scipy.stats import kruskal
import seaborn as sns
import matplotlib.pyplot as plt

# === CONFIG ===
input_folder = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Data/cleaned_data"
output_folder = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/statistical results"

variables = [
    #"birth_unm49",
    #"generation",
    "gender",
    #"birth_hdi"
]

def kruskal_effect_size(H, n, k):
    return (H - k + 1) / (n - k)

# === CREA CARTELLE ===
for var in variables:
    os.makedirs(os.path.join(output_folder, var), exist_ok=True)

# === LOOP FILE ===
for file in os.listdir(input_folder):
    if not file.endswith(".csv"):
        continue

    filepath = os.path.join(input_folder, file)
    df = pd.read_csv(filepath)
    dataset_name = file.replace(".csv", "")

    print(f"Processing {dataset_name}")

    # === LOOP VARIABILI ===
    for var in variables:
        if var not in df.columns:
            continue

        # === PREP DATA ===
        cols = [var, "total_claims"]
        if "pareto_claims" in df.columns:
            cols.append("pareto_claims")

        data = df[cols].dropna()

        if data.empty:
            continue

        # === KRUSKAL ===
        groups = [g["total_claims"].values for _, g in data.groupby(var) if len(g) > 1]
        if len(groups) < 2:
            continue

        H, p = kruskal(*groups)
        n = len(data)
        k = len(groups)
        eta2 = kruskal_effect_size(H, n, k)

        # === SAVE STATS ===
        result_row = pd.DataFrame([{
            "dataset": dataset_name,
            "variable": var,
            "H_stat": H,
            "p_value": p,
            "effect_size_eta2": eta2,
            "n_obs": n,
            "n_groups": k
        }])

        summary_path = os.path.join(output_folder, var, "summary.csv")
        if os.path.exists(summary_path):
            result_row.to_csv(summary_path, mode='a', header=False, index=False)
        else:
            result_row.to_csv(summary_path, index=False)

        #PLOTS
        has_pareto = "pareto_claims" in data.columns

        # log transform
        data["log_claims"] = np.log1p(data["total_claims"])

        # filtro gruppi piccoli
        data = data[data[var].map(data[var].value_counts()) >= 10]
        data = data[data[var].notna()]
        #if data.empty:
            #continue

        label_maps = {
            "birth_hdi": {
                "Very high human development": "Very high HDI",
                "High human development": "High HDI",
                "Medium human development": "Medium HDI",
                "Low human development": "Low HDI"
            },
            "birth_unm49": {
                "Northern America": "N. America",
                "Latin America and the Caribbean": "LatAm & Caribbean",
                "Sub-Saharan Africa": "Sub-Saharan Africa",
                "Middle Africa": "Mid. Africa",
                "Western Africa": "W. Africa",
                "Southern Europe": "South Europe",
                "Europe and Northern America": "Europe & N. America",
                "Eastern and South-Eastern Asia": "E. & SE Asia",
                "South-eastern Asia": "SE Asia",
                "Central and Southern Asia": "Central & S. Asia",
                "Western Asia": "W. Asia",
                "Australia and New Zealand": "Australia & NZ",
                # aggiungi quelli che ti servono
            }
        }

        if var in label_maps:
            data[var] = data[var].map(label_maps[var]).fillna(data[var])

        # ordine per mediana
        order = (
            data.groupby(var)["total_claims"]
            .median()
            .sort_values(ascending=False)
            .index
        )

        palette = sns.color_palette("Set2", n_colors=len(order))

        fig, axes = plt.subplots(1, 3, figsize=(22, 5))

        # Compute counts
        counts = data[var].value_counts()

        # Create new labels with counts
        new_labels = [f"{cat}\n(n={counts[cat]})" for cat in order]

        sns.boxplot(
            data=data, x=var, y="log_claims",
            order=order, hue=var,
            palette=palette,
            showfliers=False,
            ax=axes[0]
        )

        axes[0].set_xticklabels(new_labels)
        axes[0].set_title("Log distribution")

        # 2. Mean + CI
        sns.pointplot(
            data=data, x=var, y="total_claims",
            order=order, errorbar=("ci", 95),
            ax=axes[1]
        )
        axes[1].set_title("Mean + CI")

        # 3. Violin
        sns.violinplot(
            data=data, x=var, y="log_claims",
            order=order, hue=var,
            palette=palette, legend=False,
            inner="quartile",
            ax=axes[2]
        )
        axes[2].set_ylim(1, 7)
        axes[2].set_title("Violin (log)")

        # 4. Boxplot no outliers
        #sns.boxplot(
        #    data=data, x=var, y="total_claims",
        ##    order=order, hue=var,
        #    palette=palette, legend=False,
        #    showfliers=False,
        #    ax=axes[3]
        #)
        #axes[3].set_title("Boxplot (no outliers)")

        # === STRIP HEAD/TAIL ===
        if has_pareto:
            sample_data = data.sample(min(1000, len(data)))

            for ax in [axes[0], axes[2]]:
                sns.stripplot(
                    data=sample_data,
                    x=var,
                    y="log_claims" if ax == axes[0] else "total_claims",
                    order=order,
                    hue="pareto_claims",
                    alpha=0.3,
                    size=2,
                    ax=ax
                )

            handles, labels = axes[0].get_legend_handles_labels()
            fig.legend(handles, labels, title="Head vs Tail", loc="upper right")

        for ax in axes:
            ax.tick_params(axis='x', rotation=45)

        # save
        plot_path = os.path.join(output_folder, var, f"{dataset_name}.png")
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()