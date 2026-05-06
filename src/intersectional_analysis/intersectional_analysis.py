import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression


CATEGORICAL_VARS = ["birth_unm49", "gender", "generation"]


# --------------------------
# AIC / BIC
# --------------------------
def _compute_aic_bic(model, X, y):
    p = model.predict_proba(X)
    ll = np.sum(y * np.log(p[:, 1]) + (1 - y) * np.log(p[:, 0]))
    k = X.shape[1] + 1
    n = X.shape[0]
    aic = 2 * k - 2 * ll
    bic = np.log(n) * k - 2 * ll
    return aic, bic


# --------------------------
# Fit modello
# --------------------------
def _fit_model(df, vars_list, y):
    X = pd.get_dummies(df[vars_list], drop_first=True)
    model = LogisticRegression(penalty=None, solver="lbfgs", max_iter=1000)
    model.fit(X, y)
    aic, bic = _compute_aic_bic(model, X, y)
    return model, aic, bic


# --------------------------
# Selezione variabili con BIC
# --------------------------
def _select_variables_bic(df, y):
    best_vars = CATEGORICAL_VARS.copy()
    _, _, best_bic = _fit_model(df, best_vars, y)
    improved = True

    while improved and len(best_vars) > 1:
        improved = False
        results = []
        for var in best_vars:
            test_vars = [v for v in best_vars if v != var]
            _, aic, bic = _fit_model(df, test_vars, y)
            results.append((var, aic, bic, test_vars))

        results = sorted(results, key=lambda x: x[2])
        best_candidate = results[0]

        if best_candidate[2] < best_bic:
            best_vars = best_candidate[3]
            best_bic = best_candidate[2]
            improved = True
            print(f"Rimossa: {best_candidate[0]} → BIC: {best_bic:.2f}")

    print(f"✔ Variabili selezionate: {best_vars}")
    return best_vars


# --------------------------
# Prepare data
# --------------------------
def _prepare_data(file_path):
    df = pd.read_csv(file_path)
    df = df.dropna(subset=CATEGORICAL_VARS)

    if "date_of_birth" in df.columns:
        df["date_of_birth"] = df["date_of_birth"].astype(str).str.replace("+", "", regex=False)
        df["date_of_birth"] = pd.to_datetime(
            df["date_of_birth"], format="%Y-%m-%dT%H:%M:%SZ", errors="coerce"
        )
        df = df[df["date_of_birth"].dt.year > 1808]

    df = df[df["pareto_claims"].isin(["head", "long"])]
    df["pareto_claims"] = df["pareto_claims"].map({"head": 1, "long": 0})

    return df


# --------------------------
# Fit intersectional model
# --------------------------
def _fit_intersectional_model(df):
    y = df["pareto_claims"]
    selected_vars = _select_variables_bic(df, y)

    df["intersection"] = df[selected_vars].astype(str).agg("_".join, axis=1)
    counts = df["intersection"].value_counts()
    q1_threshold = counts.quantile(0.25)

    valid_intersections = counts[counts > q1_threshold].index
    df = df[df["intersection"].isin(valid_intersections)]

    df_encoded = pd.get_dummies(
        df[["intersection", "pareto_claims"]],
        columns=["intersection"],
        drop_first=True
    )
    X = df_encoded.drop(columns=["pareto_claims"])
    y = df_encoded["pareto_claims"]

    model = LogisticRegression(max_iter=1000, penalty="l1", solver="liblinear", C=0.1)
    model.fit(X, y)

    coefficients = pd.DataFrame({
        "Intersection": X.columns.str.replace("intersection_", ""),
        "Coefficient": model.coef_[0],
        "Count": [counts.get(x, 0) for x in X.columns.str.replace("intersection_", "")]
    })

    return coefficients


# --------------------------
# Plot
# --------------------------
def _plot_coefficients(coefficients, file_name):
    TOP_K = 8
    top_head = coefficients.sort_values("Coefficient", ascending=False).head(TOP_K)
    top_long = coefficients.sort_values("Coefficient", ascending=True).head(TOP_K)
    coefficients_plot = pd.concat([top_long, top_head]).sort_values("Coefficient")

    labels = [
        f"{i} (n={c})"
        for i, c in zip(coefficients_plot["Intersection"], coefficients_plot["Count"])
    ]

    plt.figure(figsize=(10, max(6, len(coefficients_plot) * 0.5)))
    plt.barh(labels, coefficients_plot["Coefficient"])
    plt.axvline(x=0, color="black")
    plt.title(f"Intersectional model — {file_name}")
    plt.xlabel("Log-odds (HEAD)")
    plt.tight_layout()


# --------------------------
# Pipeline
# --------------------------
def intersectional_logistic(file_path):
    print(f"\n--- Analizzando: {file_path} ---")

    df = _prepare_data(file_path)

    if df.empty:
        print("Dataset vuoto")
        return
    if df["pareto_claims"].nunique() < 2:
        print("Target con una sola classe → skip")
        return

    coefficients = _fit_intersectional_model(df)

    if coefficients.empty:
        print("Nessuna intersezione disponibile per il plot")
        return

    file_name = os.path.basename(file_path).replace(".csv", "")
    _plot_coefficients(coefficients, file_name)
    plt.show()


if __name__ == "__main__":
    intersectional_logistic("professions/actor.csv")