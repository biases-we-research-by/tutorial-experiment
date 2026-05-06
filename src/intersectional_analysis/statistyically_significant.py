import pandas as pd
import numpy as np
from scipy.stats import kruskal, chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import os


VARIABLES = ["gender", "birth_unm49", "birth_hdi", "generation"]

label_maps = {
    "birth_hdi": {
        "Very high human development": "Very high HDI",
        "High human development": "High HDI",
        "Medium human development": "Medium HDI",
        "Low human development": "Low HDI"
    },
    "birth_unm49": {
        "Northern America": "N. America",
        "South America": "S. America",
        "Northern Europe": "N. Europe",
        "Western Europe": "W. Europe",
        "Eastern Europe": "E. Europe",
        "South Europe": "S. Europe",
        "Latin America and the Caribbean": "LatAm & Caribbean",
        "Sub-Saharan Africa": "Sub-Saharan Africa",
        "Northern Africa": "N. Africa",
        "Middle Africa": "Mid. Africa",
        "Western Africa": "W. Africa",
        "Southern Africa": "S. Africa",
        "Eastern Africa": "E. Africa",
        "Southern Europe": "S. Europe",
        "Europe and Northern America": "Europe & N. America",
        "Eastern and South-Eastern Asia": "E. & SE Asia",
        "South-eastern Asia": "SE Asia",
        "Central and Southern Asia": "Central & S. Asia",
        "Western Asia": "W. Asia",
        "Southern Asia": "S. Asia",
        "Australia and New Zealand": "Australia & NZ",
    },
    "generation": {
        "Generation Beta": "gen. Beta",
        "Generation Alpha": "gen. Alpha",
        "Generation Z": "gen. Z",
        "Generation X": "gen. X",
        "Silent Generation": "Silent gen.",
        "Greatest Generation": "Greatest gen.",
        "Pre-Greatest Generation": "Pre-Greatest gen."
    }
}
# --------------------------
# Helpers
# --------------------------

def _kruskal_effect_size(H, n, k):
    return (H - k + 1) / (n - k)


def _prepare_data(file_path, var):
    df = pd.read_csv(file_path)

    if "date_of_birth" in df.columns:
        df["date_of_birth"] = df["date_of_birth"].astype(str).str.replace("+", "", regex=False)
        df["date_of_birth"] = pd.to_datetime(
            df["date_of_birth"], format="%Y-%m-%dT%H:%M:%SZ", errors="coerce"
        )
        df = df[df["date_of_birth"].dt.year > 1808]

    required_cols = [var, "total_claims"]
    has_pareto = "pareto_claims" in df.columns
    if has_pareto:
        required_cols.append("pareto_claims")

    data = df[required_cols].dropna(subset=required_cols).copy()
    data = data[data[var].str.strip().str.lower() != "others"]

    if data.empty:
        return None, has_pareto

    if var in label_maps:
        data[var] = data[var].map(label_maps[var]).fillna(data[var])

    if has_pareto:
        data["is_head"] = (data["pareto_claims"] == "head").astype(int)

    data["log_claims"] = np.log1p(data["total_claims"])

    return data, has_pareto


def _compute_stats(data, var, has_pareto):
    groups = [g["total_claims"].values for _, g in data.groupby(var) if len(g) > 1]
    if len(groups) < 2:
        return None

    H, p = kruskal(*groups)
    n, k = len(data), len(groups)
    eta2 = _kruskal_effect_size(H, n, k)

    chi2_p = None
    if has_pareto:
        contingency = pd.crosstab(data[var], data["pareto_claims"])
        if contingency.shape[0] > 1 and contingency.shape[1] > 1:
            chi2, chi2_p, _, _ = chi2_contingency(contingency)

    return {"H": H, "p": p, "eta2": eta2, "chi2_p": chi2_p, "n": n, "k": k}


def _compute_summary(data, var, has_pareto):
    if has_pareto:
        return data.groupby(var).agg(
            mean_claims=("total_claims", "mean"),
            median_claims=("total_claims", "median"),
            head_ratio=("is_head", "mean"),
            count=("total_claims", "size")
        ).reset_index()
    return data.groupby(var).agg(
        mean_claims=("total_claims", "mean"),
        median_claims=("total_claims", "median"),
        count=("total_claims", "size")
    ).reset_index()


def _compute_odds_ratios(data, var):
    try:
        counts_var = data[var].value_counts()
        valid_cats = counts_var[counts_var >= 10].index
        reg_data = data[data[var].isin(valid_cats)]
        if reg_data[var].nunique() > 1:
            model = smf.logit(f"is_head ~ C({var})", data=reg_data).fit(disp=0)
            return np.exp(model.params)
    except Exception as e:
        print(f"Logit failed for {var}: {e}")
    return None


def _plot_distribution(data, var):
    dist_plot = pd.crosstab(data[var], data["pareto_claims"])
    dist_plot = dist_plot.sort_values(by="head", ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    dist_plot.plot(kind="bar", stacked=True, color=["#4c72b0", "#55a868"], ax=ax)
    ax.set_title(f"Distribuzione Head vs Long per {var}")
    ax.set_ylabel("Conteggio")
    ax.set_xlabel(var)
    ax.tick_params(axis="x", rotation=90)
    ax.legend(title="Pareto Category", loc="upper right")
    plt.tight_layout()
    plt.show()

def _plot_boxplot_scatter(data, summary, var):
    threshold = summary["count"].quantile(0.0)
    filtered = summary[summary["count"] >= threshold].copy()
    valid_cats = set(filtered[var])
    data_filtered = data[data[var].isin(valid_cats)].copy()

    if data_filtered.empty or filtered.empty:
        return

    order = (
        data_filtered.groupby(var)["total_claims"]
        .median()
        .sort_values(ascending=False)
        .index
    )

    counts = data_filtered[var].value_counts()
    new_labels = [f"{cat}\n(n={counts.get(cat, 0)})" for cat in order]

    fig, axes = plt.subplots(1, 2, figsize=(16, 5))

    sns.boxplot(
        data=data_filtered, x=var, y="log_claims", order=order,
        hue=var, palette=sns.color_palette("Set2", n_colors=len(order)),
        showfliers=False, ax=axes[0]
    )
    axes[0].set_xticks(range(len(order)))
    axes[0].set_xticklabels(new_labels)
    axes[0].set_title("Log distribution")

    n_colors = filtered[var].nunique()
    palette_scatter = (
        sns.color_palette("tab20", n_colors=n_colors)
        if n_colors <= 20
        else sns.color_palette("husl", n_colors=n_colors)
    )

    sns.scatterplot(
        data=filtered, x="head_ratio", y="mean_claims",
        size="count", hue=var, sizes=(80, 500),
        palette=palette_scatter, alpha=0.75, ax=axes[1], legend="brief"
    )

    handles, labels = axes[1].get_legend_handles_labels()
    filtered_handles, filtered_labels = zip(*[
        (h, l) for h, l in zip(handles, labels)
        if l != "count" and not l.replace(".", "", 1).isdigit()
    ])
    axes[1].legend(filtered_handles, filtered_labels,
                   bbox_to_anchor=(1.05, 1), loc="upper left", frameon=True)
    axes[1].set_title("Mean Claims vs P(Head)")
    axes[1].set_xlabel("Probability of Head")
    axes[1].set_ylabel("Mean Claims")
    axes[1].grid(True, alpha=0.3)
    axes[1].margins(y=0.15)

    for ax in axes:
        ax.tick_params(axis="x", rotation=90)

    plt.tight_layout()
    plt.show()


# --------------------------
# Pipeline
# --------------------------

def analyze_file(file_path):

    for var in VARIABLES:
        data, has_pareto = _prepare_data(file_path, var)
        if data is None:
            continue

        stats = _compute_stats(data, var, has_pareto)
        if stats is None:
            continue

        summary = _compute_summary(data, var, has_pareto)

        if has_pareto:
            _compute_odds_ratios(data, var)
            _plot_distribution(data, var)

        _plot_boxplot_scatter(data, summary, var)


if __name__ == "__main__":

    analyze_file("professions/actor.csv")