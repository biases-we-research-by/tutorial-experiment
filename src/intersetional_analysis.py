import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

# --- Cartelle input/output ---
INPUT_FOLDER = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Data/cleaned_data"
OUTPUT_FOLDER = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Intersectional Logistic Regression"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# --- Variabili intersezionali ---
CATEGORICAL_VARS = [ "birth_unm49", "gender", "birth_hdi", "generation"]
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


    # 10. Selezione intersezioni rilevanti secondo threshold
    THRESHOLD = 0.6  # log-odds minimo da mostrare
    coefficients_filtered = coefficients[coefficients["Coefficient"].abs() >= THRESHOLD]


    # Controllo se ci sono dati da mostrare
    if coefficients_filtered.empty:
        print("⚠️ Nessuna intersezione supera il threshold, salto plot per questo file.")
        return

    coefficients_filtered = coefficients_filtered.sort_values(by="Coefficient", ascending=True)

    # --- Seleziona le due intersezioni più polarizzate ---
    top_head_intersections = coefficients_filtered.sort_values(by="Coefficient", ascending=False)["Intersection"].head(
        1).tolist()
    top_long_intersections = coefficients_filtered.sort_values(by="Coefficient", ascending=True)["Intersection"].head(
        1).tolist()

    # Combina tutte le intersezioni da estrarre
    polarized_intersections = top_head_intersections + top_long_intersections

    # Filtra DF originale (quello con valori pieni e date > 1808)
    df_polarized = df[df["intersection"].isin(polarized_intersections)]

    # Seleziona solo colonne richieste
    df_polarized = df_polarized[["qid", "label", "total_claims", "pareto_claims"]]

    # Salva CSV
    output_csv_polarized = os.path.join(OUTPUT_FOLDER, f"{file_name}_polarized_entities.csv")
    df_polarized.to_csv(output_csv_polarized, index=False)
    print(f"✔ CSV polarizzate salvato in: {output_csv_polarized}")

    # 11. Salva CSV
    output_csv = os.path.join(OUTPUT_FOLDER, f"{file_name}_intersectional_coefficients.csv")
    coefficients_filtered.to_csv(output_csv, index=False)
    print(f"✔ Coefficienti salvati in: {output_csv}")


    # 12. Plot
    plt.figure(figsize=(10, max(6, len(coefficients_filtered) * 0.5)))
    plt.barh(coefficients_filtered["Intersection"], coefficients_filtered["Coefficient"], color="skyblue")
    plt.axvline(x=0, color="black", linewidth=0.8)
    plt.xlabel("Effetto log-odds sulla probabilità di essere HEAD")
    plt.title(f"Intersectional Logistic Regression - {file_name}")
    plt.tight_layout()

    plot_path = os.path.join(OUTPUT_FOLDER, f"{file_name}_intersectional_plot.png")
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