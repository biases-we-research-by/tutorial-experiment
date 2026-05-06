import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.linear_model import LogisticRegression


CATEGORICAL_VARS = ["gender", "birth_unm49", "generation"]


def _prepare_data(file_path):
    df = pd.read_csv(file_path)

    cols_needed = CATEGORICAL_VARS + ["pareto_claims"]
    df = df[cols_needed].dropna()

    for var in CATEGORICAL_VARS:
        counts = df[var].value_counts()
        q1 = counts.quantile(0.0)
        valid_categories = counts[counts >= q1].index
        df = df[df[var].isin(valid_categories)]

    if "date_of_birth" in df.columns:
        df["date_of_birth"] = df["date_of_birth"].astype(str).str.replace("+", "", regex=False)
        df["date_of_birth"] = pd.to_datetime(
            df["date_of_birth"],
            format="%Y-%m-%dT%H:%M:%SZ",
            errors="coerce"
        )
        df = df[df["date_of_birth"].dt.year > 1808]

    df["pareto_claims"] = df["pareto_claims"].map({"head": 1, "long": 0})
    df = df[df["pareto_claims"].isin([0, 1])]

    return df


def _fit_model(df):
    df_encoded = pd.get_dummies(df, columns=CATEGORICAL_VARS, drop_first=True)
    X = df_encoded.drop(columns=["pareto_claims"])
    y = df_encoded["pareto_claims"]

    model = LogisticRegression(max_iter=1000, penalty="l1", solver="liblinear", C=0.1)
    model.fit(X, y)

    coefficients = pd.DataFrame({
        "Variable": X.columns,
        "Coefficient": model.coef_[0]
    })
    coefficients = coefficients[coefficients["Coefficient"].abs() > 0.0]
    coefficients = coefficients.sort_values(by="Coefficient")

    return coefficients


def _plot_coefficients(coefficients, file_name):
    def clean_label(var_name):
        for prefix in CATEGORICAL_VARS:
            if var_name.startswith(prefix + "_"):
                if var_name not in (
                    prefix + "_Unknown",
                    prefix + "_other",
                    prefix + "_Others",
                ):
                    return var_name.replace(prefix + "_", "")
        return var_name

    def assign_color(var_name):
        if var_name.startswith("gender"):       return 0
        elif var_name.startswith("birth_unm49"): return 1
        elif var_name.startswith("birth_hdi"):   return 2
        elif var_name.startswith("generation"):  return 3
        else:                                    return 4

    coefficients["Clean_Variable"] = coefficients["Variable"].apply(clean_label)
    coefficients["color_group"] = coefficients["Variable"].apply(assign_color)

    cmap = cm.get_cmap("Set2")
    colors = [cmap(i) for i in coefficients["color_group"]]
    height = max(6, len(coefficients) * 0.4)

    plt.figure(figsize=(8, height))
    plt.barh(coefficients["Clean_Variable"], coefficients["Coefficient"], color=colors)
    plt.xlabel("Likelihood of being head")
    plt.ylabel("Variables")
    plt.title(file_name)
    plt.axvline(x=0)


def analyze_file(file_path,file_name):

    df = _prepare_data(file_path)
    coefficients = _fit_model(df)

    _plot_coefficients(coefficients, file_name)
    plt.show()


if __name__ == "__main__":
    analyze_file('professions/actor.csv','logistic regression for actors')