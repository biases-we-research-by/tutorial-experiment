import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

INPUT_FOLDER = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Data/cleaned_data"
OUTPUT_FOLDER = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Results/Intersectional Logistic Regression_bic"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# --- Variabili iniziali ---
CATEGORICAL_VARS = ["birth_unm49", "gender", "generation"]
MIN_COUNT = 5   # alza un po' per evitare rumore

# --------------------------
# AIC / BIC
# --------------------------
def compute_aic_bic(model, X, y):
    p = model.predict_proba(X)
    ll = np.sum(y*np.log(p[:,1]) + (1-y)*np.log(p[:,0]))
    k = X.shape[1] + 1
    n = X.shape[0]
    aic = 2*k - 2*ll
    bic = np.log(n)*k - 2*ll
    return aic, bic

# --------------------------
# Fit modello
# --------------------------
def fit_model(df, vars_list, y):
    X = pd.get_dummies(df[vars_list], drop_first=True)
    model = LogisticRegression(penalty=None, solver='lbfgs', max_iter=1000)
    model.fit(X, y)
    aic, bic = compute_aic_bic(model, X, y)
    return model, aic, bic

# --------------------------
# Selezione variabili con BIC
# --------------------------
def select_variables_bic(df, y):
    remaining_vars = CATEGORICAL_VARS.copy()
    best_vars = remaining_vars.copy()

    _, best_aic, best_bic = fit_model(df, best_vars, y)

    improved = True

    while improved and len(best_vars) > 1:
        improved = False
        results = []

        for var in best_vars:
            test_vars = [v for v in best_vars if v != var]
            _, aic, bic = fit_model(df, test_vars, y)
            results.append((var, aic, bic, test_vars))

        results = sorted(results, key=lambda x: x[2])  # BIC
        best_candidate = results[0]

        if best_candidate[2] < best_bic:
            removed_var = best_candidate[0]
            best_vars = best_candidate[3]
            best_aic = best_candidate[1]
            best_bic = best_candidate[2]
            improved = True
            print(f"Rimossa: {removed_var} → BIC: {best_bic:.2f}")

    print(f"✔ Variabili selezionate: {best_vars}")
    return best_vars

# --------------------------
# Analisi principale
# --------------------------
def intersectional_logistic(file_path):
    file_name = os.path.basename(file_path).replace(".csv", "")
    print(f"\n--- Analizzando: {file_name} ---")

    df = pd.read_csv(file_path)
    df = df.dropna(subset=CATEGORICAL_VARS)

    # Filtro date
    if "date_of_birth" in df.columns:
        df["date_of_birth"] = df["date_of_birth"].astype(str).str.replace("+", "", regex=False)
        df["date_of_birth"] = pd.to_datetime(df["date_of_birth"], format="%Y-%m-%dT%H:%M:%SZ", errors="coerce")
        df = df[df["date_of_birth"].dt.year > 1808]

    # Target
    df = df[df["pareto_claims"].isin(["head", "long"])]
    df["pareto_claims"] = df["pareto_claims"].map({"head": 1, "long": 0})

    if df.empty:
        print("⚠️ Dataset vuoto")
        return

    print("\nDistribuzione gender vs pareto_claims (percentuali):")
    print(pd.crosstab(df["gender"], df["pareto_claims"], normalize="index"))

    print("\nConteggi assoluti:")
    print(pd.crosstab(df["gender"], df["pareto_claims"]))

    y = df["pareto_claims"]

    # --------------------------
    # STEP 1: selezione variabili
    # --------------------------
    selected_vars = select_variables_bic(df, y)

    # --------------------------
    # STEP 2: crea intersezioni
    # --------------------------
    df["intersection"] = df[selected_vars].astype(str).agg("_".join, axis=1)


    counts = df["intersection"].value_counts()

    # Calcolo quartile inferiore (Q1)
    q1_threshold = counts.quantile(0.25)

    print(f"\nQuartile 1 (Q1) soglia: {q1_threshold}")

    valid_intersections = counts[counts > q1_threshold].index

    df = df[df["intersection"].isin(valid_intersections)]

    print(f"Intersezioni totali: {len(counts)}")
    print(f"Intersezioni mantenute (>Q1): {len(valid_intersections)}")

    if df.empty:
        print("Nessuna intersezione valida")
        return
    if df["intersection"].nunique() < 2:
        print("⚠️ Una sola intersezione dopo filtro → skip categoria")
        return
    # --------------------------
    # STEP 3: regressione intersezionale
    # --------------------------
    df_encoded = pd.get_dummies(df[["intersection", "pareto_claims"]],
                                columns=["intersection"],
                                drop_first=True)

    X = df_encoded.drop(columns=["pareto_claims"])
    y = df_encoded["pareto_claims"]

    model = LogisticRegression(max_iter=1000, penalty="l1", solver="liblinear", C=0.1)
    model.fit(X, y)

    coefficients = pd.DataFrame({
        "Intersection": X.columns.str.replace("intersection_", ""),
        "Coefficient": model.coef_[0],
        "Count": [counts.get(x, 0) for x in X.columns.str.replace("intersection_", "")]
    })

    # --------------------------
    # Selezione Top K intersezioni
    # --------------------------
    TOP_K = 10

    top_head = coefficients.sort_values(by="Coefficient", ascending=False).head(TOP_K)
    top_long = coefficients.sort_values(by="Coefficient", ascending=True).head(TOP_K)

    top_combined = pd.concat([top_head, top_long])

    print("\nTop intersezioni HEAD:")
    print(top_head)

    print("\nTop intersezioni LONG:")
    print(top_long)

    coefficients = coefficients.sort_values(by="Coefficient")
    TOP_K_SELECTION = 10  # puoi cambiarlo

    top_head_intersections = coefficients.sort_values(
        by="Coefficient", ascending=False
    ).head(TOP_K_SELECTION)["Intersection"].tolist()

    top_long_intersections = coefficients.sort_values(
        by="Coefficient", ascending=True
    ).head(TOP_K_SELECTION)["Intersection"].tolist()

    # Filtra entità
    df_head = df[df["intersection"].isin(top_head_intersections)].copy()
    df_long = df[df["intersection"].isin(top_long_intersections)].copy()

    # Aggiungi label head_intersection
    df_head["head_intersection"] = 1
    df_long["head_intersection"] = 0

    # Sampling (max 500 per gruppo)
    df_head_sample = df_head.sample(n=min(500, len(df_head)), random_state=42)
    df_long_sample = df_long.sample(n=min(500, len(df_long)), random_state=42)

    # Unisci
    df_final_sample = pd.concat([df_head_sample, df_long_sample])

    # Se vuoi esattamente 1000 (quando possibile)
    if len(df_final_sample) > 1000:
        df_final_sample = df_final_sample.sample(n=1000, random_state=42)

    # Seleziona colonne richieste
    cols_to_save = [
        "qid",
        "label",
        "intersection",
        "head_intersection",
        "pareto_claims",
        "total_claims"
    ]

    cols_to_save = [c for c in cols_to_save if c in df_final_sample.columns]

    df_final_sample = df_final_sample[cols_to_save]

    # Salva CSV
    sample_output_path = os.path.join(
        OUTPUT_FOLDER,
        f"{file_name}_top_bottom_1000.csv"
    )

    df_final_sample.to_csv(sample_output_path, index=False)

    print(f"✔ Salvato sample 1000 entità: {sample_output_path}")
    # --------------------------
    # OUTPUT
    # --------------------------
    output_csv = os.path.join(OUTPUT_FOLDER, f"{file_name}_coefficients.csv")
    coefficients.to_csv(output_csv, index=False)

    print(f"✔ Salvato CSV: {output_csv}")

    # --------------------------
    # Selezione dinamica Top intersezioni per plot
    # --------------------------
    TOP_K = 8  # per lato (head / long)

    # Top head (coef più alti)
    top_head = coefficients.sort_values(by="Coefficient", ascending=False).head(TOP_K)

    # Top long (coef più bassi)
    top_long = coefficients.sort_values(by="Coefficient", ascending=True).head(TOP_K)

    # Combina
    coefficients_plot = pd.concat([top_long, top_head])

    # Ordina per plot (dal più negativo al più positivo)
    coefficients_plot = coefficients_plot.sort_values(by="Coefficient")

    if coefficients_plot.empty:
        print("⚠️ Nessuna intersezione disponibile per il plot")
        return

    # --------------------------
    # Plot
    # --------------------------
    plt.figure(figsize=(10, max(6, len(coefficients_plot) * 0.5)))

    # Label con count (molto importante)
    labels = [
        f"{i} (n={c})"
        for i, c in zip(coefficients_plot["Intersection"], coefficients_plot["Count"])
    ]

    plt.barh(labels, coefficients_plot["Coefficient"])
    plt.axvline(x=0, color="black")

    plt.title(f"Intersectional Model - {file_name}")
    plt.xlabel("Log-odds (HEAD)")

    plt.tight_layout()

    plot_path = os.path.join(OUTPUT_FOLDER, f"{file_name}_plot.png")
    plt.savefig(plot_path)
    plt.close()

    print(f"✔ Salvato plot: {plot_path}")

# --------------------------
# LOOP
# --------------------------
for file in os.listdir(INPUT_FOLDER):
    if file.endswith(".csv"):
        intersectional_logistic(os.path.join(INPUT_FOLDER, file))

print("Analisi completata")