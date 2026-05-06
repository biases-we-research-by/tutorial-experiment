import os
import pandas as pd
import numpy as np
from scipy.stats import kruskal, chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from src.utils.mapping import label_maps

input_folder = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Data/cleaned_data"
output_folder = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Results/Kruskal-wallis & means"

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

for file in os.listdir(input_folder):
    if not file.endswith(".csv"):
        continue

    filepath = os.path.join(input_folder, file)
    df = pd.read_csv(filepath)

    # -----------------------------
    # FILTER: date_of_birth > 1808
    # -----------------------------
    if "date_of_birth" in df.columns:
        # Rimuove il "+" iniziale (formato Wikidata)
        df["date_of_birth"] = df["date_of_birth"].astype(str).str.replace("+", "", regex=False)

        # Parsing esplicito (molto più veloce e sicuro)
        df["date_of_birth"] = pd.to_datetime(
            df["date_of_birth"],
            format="%Y-%m-%dT%H:%M:%SZ",
            errors="coerce"
        )
        print(df["date_of_birth"].head())
        df = df[df["date_of_birth"].dt.year > 1808]

    dataset_name = file.replace(".csv", "")

    print(f"Processing {dataset_name}")

    for var in variables:
        if var not in df.columns:
            continue

        required_cols = [var, "total_claims"]

        if "pareto_claims" in df.columns:
            required_cols.append("pareto_claims")

        data = df[required_cols].dropna(subset=required_cols).copy()

        data = data[data[var].str.strip().str.lower() != "others"]
        if data.empty:
            continue

        if var in label_maps:
            data[var] = data[var].map(label_maps[var]).fillna(data[var])

# KRUSKAL sulle medie

        groups = [g["total_claims"].values for _, g in data.groupby(var) if len(g) > 1]
        if len(groups) < 2:
            continue

        H, p = kruskal(*groups)
        n = len(data)
        k = len(groups)
        eta2 = kruskal_effect_size(H, n, k)

# Chi-square tra head and tail (pareto claims)
        has_pareto = "pareto_claims" in data.columns

        if has_pareto:
            data["is_head"] = (data["pareto_claims"] == "head").astype(int)

        chi2_p = None
        if has_pareto:
            contingency = pd.crosstab(data[var], data["pareto_claims"])
            if contingency.shape[0] > 1 and contingency.shape[1] > 1:
                chi2, chi2_p, _, _ = chi2_contingency(contingency)

# logistic regression su head and claim
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

# Distribuzione head vs claim
        if has_pareto:
            # Crea crosstab
            dist_plot = pd.crosstab(data[var], data["pareto_claims"])
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

# PLOTS
        # PLOTS
        data["log_claims"] = np.log1p(data["total_claims"])

        # filtro minimo numerosità
        data = data[data[var].map(data[var].value_counts()) >= 1]
        if data.empty:
            continue

        # --- 1. Filtro Q1 su summary ---
        threshold = summary["count"].quantile(0.0)
        filtered = summary[summary["count"] >= threshold].copy()

        # categorie valide (coerenza tra grafici)
        valid_cats = set(filtered[var])

        # filtra anche data
        data_filtered = data[data[var].isin(valid_cats)].copy()

        if data_filtered.empty or filtered.empty:
            continue

        # --- 2. Ordine coerente ---
        order = (
            data_filtered.groupby(var)["total_claims"]
            .median()
            .sort_values(ascending=False)
            .index
        )

        # --- 3. Conteggi per label ---
        counts = data_filtered[var].value_counts()
        new_labels = [f"{cat}\n(n={counts.get(cat, 0)})" for cat in order]

        # --- 4. Setup figura ---
        fig, axes = plt.subplots(1, 2, figsize=(16, 5))

        # --- 5. BOXPLOT ---
        palette_box = sns.color_palette("Set2", n_colors=len(order))

        sns.boxplot(
            data=data_filtered,
            x=var,
            y="log_claims",
            order=order,
            hue=var,
            palette=palette_box,
            showfliers=False,
            ax=axes[0]
        )

        axes[0].set_xticks(range(len(order)))
        axes[0].set_xticklabels(new_labels)
        axes[0].set_title("Log distribution")
        #axes[0].legend().remove()  # rimuove legenda duplicata

        # --- 6. SCATTER ---
        n_colors = filtered[var].nunique()
        palette_scatter = (
            sns.color_palette("tab20", n_colors=n_colors)
            if n_colors <= 20
            else sns.color_palette("husl", n_colors=n_colors)
        )

        sns.scatterplot(
            data=filtered,
            x="head_ratio",
            y="mean_claims",
            size="count",
            hue=var,
            sizes=(80, 500),
            palette=palette_scatter,
            alpha=0.75,
            ax=axes[1],
            legend="brief"
        )

        # --- 7. Legenda SOLO per hue ---
        # prende legenda completa
        handles, labels = axes[1].get_legend_handles_labels()

        # rimuove la parte relativa a "size" (count)
        filtered_handles = []
        filtered_labels = []
        for h, l in zip(handles, labels):
            if l != "count" and not l.replace('.', '', 1).isdigit():
                filtered_handles.append(h)
                filtered_labels.append(l)

        axes[1].legend(
            filtered_handles,
            filtered_labels,
            #title=var,
            bbox_to_anchor=(1.05, 1),
            loc="upper left",
            frameon=True
        )
        axes[1].set_title("Mean Claims vs P(Head)")
        axes[1].set_xlabel("Probability of Head")
        axes[1].set_ylabel("Mean Claims")
        axes[1].grid(True, alpha=0.3)
        axes[1].margins(y=0.15)

        # rotazione label
        for ax in axes:
            ax.tick_params(axis='x', rotation=90)

        # --- 9. Save ---
        plot_path = os.path.join(output_folder, var, f"{dataset_name}.png")
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()