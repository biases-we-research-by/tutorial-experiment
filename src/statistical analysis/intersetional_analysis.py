import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

INPUT_FOLDER = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Data/cleaned_data"
OUTPUT_FOLDER = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Results/Intersectional Logistic Regression"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# --- Variabili intersezionali ---
CATEGORICAL_VARS = [ "birth_unm49", "gender", "generation"]
MIN_COUNT = 1      # minimo numero di entità per combinazione
TOP_K = 10          # top K intersezioni positive/negative da mostrare

# --------------------------
# Funzione per analisi intersezionale + regressione
# --------------------------
def intersectional_logistic(file_path):
    file_name = os.path.basename(file_path).replace(".csv", "")
    print(f"\n--- Analizzando: {file_name} ---")

    # 1. Carica CSV
    df = pd.read_csv(file_path)

    # 2. Drop righe con valori mancanti nelle variabili intersezionali
    df = df.dropna(subset=CATEGORICAL_VARS)

    # 3. Filtro data > 1808
    if "date_of_birth" in df.columns:
        df["date_of_birth"] = df["date_of_birth"].astype(str).str.replace("+", "", regex=False)
        df["date_of_birth"] = pd.to_datetime(
            df["date_of_birth"],
            format="%Y-%m-%dT%H:%M:%SZ",
            errors="coerce"
        )
        df = df[df["date_of_birth"].dt.year > 1808]

    # 5. Crea variabile intersezionale (UNA SOLA VOLTA, qui)
    df["intersection"] = df[CATEGORICAL_VARS].astype(str).agg("_".join, axis=1)

    # 6. Conteggi
    counts = df["intersection"].value_counts()

    # --- Quartile robusto ---
    import numpy as np

    q1_threshold = np.percentile(counts.values, 25)
    q1_threshold = int(np.floor(q1_threshold))  # evita problemi float

    print(f"\nQuartile 1 (Q1) soglia (arrotondata): {q1_threshold}")

    # --- Filtro ---
    valid_intersections = counts[counts > q1_threshold].index
    df = df[df["intersection"].isin(valid_intersections)]

    print(f"Intersezioni totali: {len(counts)}")
    print(f"Intersezioni mantenute (>Q1): {len(valid_intersections)}")

    # Check sicurezza
    if df.empty:
        print("Nessuna intersezione valida")
        return

    if df["intersection"].nunique() < 2:
        print("⚠️ Una sola intersezione dopo filtro → skip categoria")
        return

    # 4. Target binario: head=1, long=0
    df["pareto_claims"] = df["pareto_claims"].map({
        "head": 1,
        "long": 0
    })
    df = df[df["pareto_claims"].isin([0, 1])]

    # 5. Crea variabile intersezionale
    df["intersection"] = df[CATEGORICAL_VARS].astype(str).agg("_".join, axis=1)

    # 6. Filtra combinazioni rare
    counts = df["intersection"].value_counts()
    valid_intersections = counts[counts >= MIN_COUNT].index
    df = df[df["intersection"].isin(valid_intersections)]

    if df.empty:
        print("⚠️ Nessuna intersezione con abbastanza entità, salto file.")
        return

    # 7. One-hot encoding della variabile intersezionale
    df_encoded = pd.get_dummies(df[["intersection", "pareto_claims"]], columns=["intersection"], drop_first=True)

    X = df_encoded.drop(columns=["pareto_claims"])
    y = df_encoded["pareto_claims"]

    # 8. Logistic Regression con L1
    model = LogisticRegression(
        max_iter=1000,
        penalty="l1",
        solver="liblinear",
        C=0.1
    )
    model.fit(X, y)

    # 9. Coefficienti
    coefficients = pd.DataFrame({
        "Intersection": X.columns.str.replace("intersection_", ""),
        "Coefficient": model.coef_[0],
        "Count": [counts.get(x, 0) for x in X.columns.str.replace("intersection_", "")]
    })

    # 10. Selezione top intersezioni (senza threshold fisso)

    TOP_K = 10  # puoi cambiarlo

    # Ordina coefficienti
    coefficients_sorted = coefficients.sort_values(by="Coefficient")

    # Top negativi (LONG)
    top_long = coefficients_sorted.head(TOP_K)

    # Top positivi (HEAD)
    top_head = coefficients_sorted.tail(TOP_K)

    # Combina
    coefficients_plot = pd.concat([top_long, top_head])

    # Se per qualche motivo è vuoto
    if coefficients_plot.empty:
        print("⚠️ Nessuna intersezione disponibile per il plot")
        return

    # --------------------------
    # Estrai intersezioni polarizzate per CSV
    # --------------------------
    polarized_intersections = coefficients_plot["Intersection"].tolist()

    df_polarized = df[df["intersection"].isin(polarized_intersections)].copy()

    # Seleziona solo colonne richieste
    cols = ["qid", "label", "total_claims", "pareto_claims", "intersection"]
    cols = [c for c in cols if c in df_polarized.columns]

    df_polarized = df_polarized[cols]

    # Salva CSV
    output_csv_polarized = os.path.join(
        OUTPUT_FOLDER, f"{file_name}_polarized_entities.csv"
    )
    df_polarized.to_csv(output_csv_polarized, index=False)

    print(f"✔ CSV polarizzate salvato in: {output_csv_polarized}")

    # --------------------------
    # Salva coefficienti COMPLETI (non filtrati!)
    # --------------------------
    output_csv = os.path.join(
        OUTPUT_FOLDER, f"{file_name}_intersectional_coefficients.csv"
    )
    coefficients.to_csv(output_csv, index=False)

    print(f"✔ Coefficienti salvati in: {output_csv}")

    # --------------------------
    # Plot
    # --------------------------
    plt.figure(figsize=(10, max(6, len(coefficients_plot) * 0.5)))

    # Ordina per visualizzazione
    coefficients_plot = coefficients_plot.sort_values(by="Coefficient")

    # Label con count (molto utile!)
    labels = [
        f"{i} (n={c})"
        for i, c in zip(coefficients_plot["Intersection"], coefficients_plot["Count"])
    ]

    plt.barh(labels, coefficients_plot["Coefficient"])
    plt.axvline(x=0, color="black", linewidth=0.8)

    plt.xlabel("Log-odds (HEAD)")
    plt.title(f"Top Intersection Effects - {file_name}")

    plt.tight_layout()

    plot_path = os.path.join(
        OUTPUT_FOLDER, f"{file_name}_intersectional_plot.png"
    )
    plt.savefig(plot_path)
    plt.close()

    print(f"✔ Plot salvato in: {plot_path}")

# --------------------------
# Loop su tutti i file CSV
# --------------------------
for file in os.listdir(INPUT_FOLDER):
    if file.endswith(".csv"):
        file_path = os.path.join(INPUT_FOLDER, file)
        intersectional_logistic(file_path)

print("\n🎯 Analisi intersezionale completata su tutti i file!")