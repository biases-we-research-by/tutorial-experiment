
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.linear_model import LogisticRegression


# Cartella input
INPUT_FOLDER = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Data/cleaned_data"

# Cartella output
OUTPUT_FOLDER = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Logistic Regression results"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Variabili da usare
CATEGORICAL_VARS = ["gender", "birth_unm49", "birth_hdi", "generation"]


def analyze_file(file_path):
    print(f"\n--- Analizzando: {file_path} ---")


    df = pd.read_csv(file_path)

    cols_needed = CATEGORICAL_VARS + ["pareto_claims"]
    df = df[cols_needed]

    df = df.dropna()

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

    # Target binario: head=1, long=0
    df["pareto_claims"] = df["pareto_claims"].map({
        "head": 1,
        "long": 0
    })

    # Rimuove eventuali valori non validi
    df = df[df["pareto_claims"].isin([0, 1])]

    df_encoded = pd.get_dummies(
        df,
        columns=CATEGORICAL_VARS,
        drop_first=True  # evita multicollinearità
    )

    # ============================
    # 5. DEFINIZIONE X e y
    # ============================

    X = df_encoded.drop(columns=["pareto_claims"])
    y = df_encoded["pareto_claims"]

    # ============================
    # 6. MODELLO LOGISTICO
    # ============================

    model = LogisticRegression(
        max_iter=1000,
        penalty="l1",
        solver="liblinear",
        C=0.1
    )
    model.fit(X, y)

    # ============================
    # 7. COEFFICIENTI
    # ============================

    coefficients = pd.DataFrame({
        "Variable": X.columns,
        "Coefficient": model.coef_[0]
    })

    # Ordina per importanza
    coefficients = coefficients.sort_values(by="Coefficient")

    THRESHOLD = 0.05  # puoi regolarlo

    coefficients = coefficients[
        coefficients["Coefficient"].abs() > THRESHOLD
        ]


    file_name = os.path.basename(file_path).replace(".csv", "")

    # Salva coefficienti
    coeff_path = os.path.join(OUTPUT_FOLDER, f"{file_name}_coefficients.csv")
    coefficients.to_csv(coeff_path, index=False)

    print(f"✔ Coefficienti salvati in: {coeff_path}")


    # Funzione per pulire i nomi delle variabili
    def clean_label(var_name):
        for prefix in CATEGORICAL_VARS:
            if var_name.startswith(prefix + "_"):
                print(var_name)
                if (var_name != prefix + "_Unknown" and
                var_name != prefix + "_other" and
                var_name != prefix + "_Others"):
                    return var_name.replace(prefix + "_", "")
        return var_name  # per variabili numeriche tipo total_claims

    # Applica label pulite
    coefficients["Clean_Variable"] = coefficients["Variable"].apply(clean_label)

    def assign_color(var_name):
        if var_name.startswith("gender"):
            return 0
        elif var_name.startswith("birth_unm49"):
            return 1
        elif var_name.startswith("birth_hdi"):
            return 2
        elif var_name.startswith("generation"):
            return 3
        else:
            return 4  # total_claims o altro

    coefficients["color_group"] = coefficients["Variable"].apply(assign_color)

    cmap = cm.get_cmap("Set2")  # you can use 'Set1', 'tab20', etc.
    colors = [cmap(i) for i in coefficients["color_group"]]

    height = max(6, len(coefficients) * 0.4)

    plt.figure(figsize=(8, height))

    plt.barh(
        coefficients["Clean_Variable"],
        coefficients["Coefficient"],
        color=colors
    )

    plt.xlabel("Effetto sulla probabilità di essere HEAD")
    plt.ylabel("Variabili")
    plt.title(f"Feature Impact - {file_name}")

    # Linea verticale per zero (molto utile visivamente)
    plt.axvline(x=0)


    plot_path = os.path.join(OUTPUT_FOLDER, f"{file_name}_plot.png")
    plt.savefig(plot_path, bbox_inches="tight")
    plt.close()

    print(f"✔ Plot salvato in: {plot_path}")


for file in os.listdir(INPUT_FOLDER):
    if file.endswith(".csv"):
        file_path = os.path.join(INPUT_FOLDER, file)
        analyze_file(file_path)

print("\n🎯 Analisi completata su tutti i file!")