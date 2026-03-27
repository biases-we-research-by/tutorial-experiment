import os
import pandas as pd
import numpy as np
from scipy.stats import kruskal, chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from mapping import label_maps

# === CONFIG ===
input_folder = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Data/cleaned_data"
output_folder = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/statistical results2"

variables = [
    "gender",
    "birth_unm49",
    "birth_hdi",
    "generation",
]

def kruskal_effect_size(H, n, k):
    return (H - k + 1) / (n - k)

label_maps = label_maps

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

        if var in label_maps:
            data[var] = data[var].map(label_maps[var]).fillna(data[var])

        # ===============================
        # KRUSKAL
        # ===============================
        groups = [g["total_claims"].values for _, g in data.groupby(var) if len(g) > 1]
        if len(groups) < 2:
            continue

        H, p = kruskal(*groups)
        n = len(data)
        k = len(groups)
        eta2 = kruskal_effect_size(H, n, k)

        # ===============================
        # BINARIZZAZIONE HEAD
        # ===============================
        has_pareto = "pareto_claims" in data.columns

        if has_pareto:
            data["is_head"] = (data["pareto_claims"] == "head").astype(int)

        # ===============================
        # CHI-SQUARE
        # ===============================
        chi2_p = None
        if has_pareto:
            contingency = pd.crosstab(data[var], data["pareto_claims"])
            if contingency.shape[0] > 1 and contingency.shape[1] > 1:
                chi2, chi2_p, _, _ = chi2_contingency(contingency)

        # ===============================
        # LOGISTIC REGRESSION
        # ===============================
        if has_pareto:
            try:
                # Remove rare categories
                counts_var = data[var].value_counts()
                valid_cats = counts_var[counts_var >= 10].index
                reg_data = data[data[var].isin(valid_cats)]

                if reg_data[var].nunique() > 1:
                    model = smf.logit(f"is_head ~ C({var})", data=reg_data).fit(disp=0)
                    odds_ratios = np.exp(model.params)
                else:
                    odds_ratios = None

            except Exception as e:
                print(f"Logit failed for {var} in {dataset_name}: {e}")
                odds_ratios = None

        # ===============================
        # TABELLA AGGREGATA
        # ===============================
        if has_pareto:
            summary = data.groupby(var).agg(
                mean_claims=("total_claims", "mean"),
                median_claims=("total_claims", "median"),
                head_ratio=("is_head", "mean"),
                count=("total_claims", "size")
            ).reset_index()
        else:
            summary = data.groupby(var).agg(
                mean_claims=("total_claims", "mean"),
                median_claims=("total_claims", "median"),
                count=("total_claims", "size")
            ).reset_index()

        # ===============================
        # DISTRIBUZIONE HEAD vs LONG
        # ===============================
        if has_pareto:
            # Crea crosstab
            dist_plot = pd.crosstab(data[var], data["pareto_claims"])
            # Ordina per numero di head decrescente
            dist_plot = dist_plot.sort_values(by="head", ascending=False)

            # Plot stacked bar con conteggi assoluti
            plt.figure(figsize=(8, 5))
            dist_plot.plot(kind="bar", stacked=True, color=["#4c72b0", "#55a868"])

            plt.title(f"Distribuzione Head vs Long per {var}")
            plt.ylabel("Conteggio")
            plt.xlabel(var)
            plt.xticks(rotation=90)
            plt.legend(title="Pareto Category", loc="upper right")

            dist_plot_path = os.path.join(output_folder, var, f"{dataset_name}_head_long_distribution.png")
            plt.tight_layout()
            plt.savefig(dist_plot_path)
            plt.close()

        # SAVE SUMMARY
        summary_path = os.path.join(output_folder, var, f"{dataset_name}_group_summary.csv")
        summary.to_csv(summary_path, index=False)

        # ===============================
        # SAVE GLOBAL STATS
        # ===============================
        result_row = pd.DataFrame([{
            "dataset": dataset_name,
            "variable": var,
            "H_stat": H,
            "p_value": p,
            "effect_size_eta2": eta2,
            "chi2_p_value": chi2_p,
            "n_obs": n,
            "n_groups": k
        }])

        summary_global_path = os.path.join(output_folder, var, "summary_global.csv")
        if os.path.exists(summary_global_path):
            result_row.to_csv(summary_global_path, mode='a', header=False, index=False)
        else:
            result_row.to_csv(summary_global_path, index=False)

        # ===============================
        # PREP PLOT BOX + SCATTER
        # ===============================
        data["log_claims"] = np.log1p(data["total_claims"])
        data = data[data[var].map(data[var].value_counts()) >= 10]
        if data.empty:
            continue

        order = (
            data.groupby(var)["total_claims"]
            .median()
            .sort_values(ascending=False)
            .index
        )
        palette = sns.color_palette("Set2", n_colors=len(order))

        # PLOT BOX + SCATTER
        fig, axes = plt.subplots(1, 2, figsize=(16, 5))

        counts = data[var].value_counts()
        new_labels = [f"{cat}\n(n={counts[cat]})" for cat in order]

        # BOXPLOT
        sns.boxplot(
            data=data, x=var, y="log_claims",
            order=order, hue=var,
            palette=palette,
            showfliers=False,
            ax=axes[0]
        )
        axes[0].set_xticks(range(len(order)))
        axes[0].set_xticks(range(len(order)))
        axes[0].set_xticklabels(new_labels)
        axes[0].set_title("Log distribution")

        # SCATTER
        if has_pareto:
            sns.scatterplot(
                data=summary,
                x="head_ratio",
                y="mean_claims",
                size="count",
                hue=var,
                sizes=(80, 500),
                alpha=0.85,
                ax=axes[1],
                legend="brief"
            )
            axes[1].set_title("Mean Claims vs P(Head)")
            axes[1].set_xlabel("Probability of Head")
            axes[1].set_ylabel("Mean Claims")
            axes[1].grid(True, alpha=0.3)
            axes[1].margins(y=0.15)

            #handles, labels = axes[1].get_legend_handles_labels()
            #valid_labels = summary[var].astype(str).unique()
            #new_handles, new_labels = zip(*[(h,l) for h,l in zip(handles, labels) if l in valid_labels])
            axes[1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        for ax in axes:
            ax.tick_params(axis='x', rotation=90)

        # SAVE BOX + SCATTER
        plot_path = os.path.join(output_folder, var, f"{dataset_name}.png")
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()