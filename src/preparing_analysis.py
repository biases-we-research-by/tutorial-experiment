import os
import json
import pandas as pd
import ast
from mapping import unm49_mapping

BASE_DIR = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Data/raw data"


# -----------------------
# Utility
# -----------------------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_label(labels, lang="en"):
    for l in labels:
        if l["language"] == lang:
            return l["value"]
    return None


# -----------------------
# MAIN
# -----------------------
def process_category(cat_path, cat_name):
    print(f"\nProcessing: {cat_name}")

    # ---- PATH ----
    countries_path = os.path.join(cat_path, "countries.json")
    entity_json_path = os.path.join(cat_path, f"{cat_name}.json")
    pareto_path = os.path.join(cat_path, "pareto.csv")
    #unm49_path = os.path.join(cat_path, unm49_mapping)

    # ---- LOAD ----
    countries = load_json(countries_path)
    entities = load_json(entity_json_path)
    #unm49_mapping = load_json(unm49_path)

    # -----------------------
    # COUNTRY MAP
    # -----------------------
    country_map = {}
    for c in countries:
        qid = c["entity"]
        label = extract_label(c["labels"])
        country_map[qid] = label

    # -----------------------
    # ENTITY LABEL MAP (PER P69 ecc.)
    # -----------------------
    entity_label_map = {}
    for e in entities:
        entity_label_map[e["entity"]] = extract_label(e["labels"])

    # -----------------------
    # BASE DF
    # -----------------------
    rows = []
    for e in entities:
        qid = e["entity"]

        rows.append({
            "qid": qid,
            "label": extract_label(e["labels"]),
            "date_of_birth": e.get("entity_claims", {}).get("P569", [None])[0],
            "total_claims": e.get("total_claims"),
            "external_ids": e.get("external_ids")
        })

    df = pd.DataFrame(rows)

    # -----------------------
    # PARETO
    # -----------------------
    pareto = pd.read_csv(pareto_path)
    pareto["qid"] = pareto["entity"].apply(lambda x: ast.literal_eval(x)["entity"])
    pareto = pareto[["qid", "c_claims", "pareto_ext"]]

    df = df.merge(pareto, on="qid", how="left")

    # -----------------------
    # CITIZENSHIP
    # -----------------------
    cit_path = os.path.join(cat_path, "P27.csv")
    if os.path.exists(cit_path):
        cit = pd.read_csv(cit_path)
        cit.columns = ["qid", "citizenship"]

        df = df.merge(cit, on="qid", how="left")
        df["citizenship_label"] = df["citizenship"].map(country_map)

    # -----------------------
    # PLACE OF BIRTH
    # -----------------------
    pob_path = os.path.join(cat_path, "P19.csv")
    if os.path.exists(pob_path):
        pob = pd.read_csv(pob_path)

        pob = pob.rename(columns={
            "entity": "qid",
            "country": "pob_country",
            "countryLabel": "place_of_birth_country_label",
            "hdi": "place_of_birth_country_label_hdi"
        })

        df = df.merge(
            pob[[
                "qid",
                "pob_country",
                "place_of_birth_country_label",
                "place_of_birth_country_label_hdi"
            ]],
            on="qid",
            how="left"
        )

    # -----------------------
    # EDUCATED AT (P69 + LABEL ISTITUTO)
    # -----------------------
    edu_path = os.path.join(cat_path, "P69.csv")

    if os.path.exists(edu_path):
        edu = pd.read_csv(edu_path)

        edu = edu.rename(columns={
            "entity": "qid",
            "P69": "educated_at_qid",
            "country": "edu_country",
            "countryLabel": "educated_at_country_label",
            "hdi": "educated_at_country_label_hdi"
        })

        # 🔥 aggiungi label istituto
        edu["educated_at_label"] = edu["educated_at_qid"].map(country_map)

        df = df.merge(
            edu[[
                "qid",
                "educated_at_label",
                "educated_at_country_label",
                "educated_at_country_label_hdi"
            ]],
            on="qid",
            how="left"
        )

    # -----------------------
    # GENDER
    # -----------------------
    gender_path = os.path.join(cat_path, "P21.csv")

    if os.path.exists(gender_path):
        gender = pd.read_csv(gender_path)

        gender = gender.rename(columns={
            "entity": "qid",
            "P21": "gender_qid"
        })


        gender_map = {
            "Q6581097": "male",
            "Q6581072": "female",
            "Q48270": "other",
            "Q121307094": "other",
            "Q2449503": "other",
            "Q1052281": "other",
            "Q189125": "other"
        }

        gender["gender"] = gender["gender_qid"].map(gender_map)
        gender = gender[["qid", "gender"]]

        df = df.merge(gender, on="qid", how="left")

    # -----------------------
    # UNM49 MAPPING
    # -----------------------
    if "place_of_birth_country_label" in df.columns:
        df["unm49"] = df["place_of_birth_country_label"].map(unm49_mapping)

    # -----------------------
    # CLEANING
    # -----------------------
    df = df.replace("{}", pd.NA)

    # -----------------------
    # REMOVE DUPLICATES
    # -----------------------
    df["non_null_count"] = df.notna().sum(axis=1)
    df = df.sort_values(["qid", "non_null_count"], ascending=[True, False])
    df = df.drop_duplicates(subset="qid", keep="first")
    df = df.drop(columns=["non_null_count"])

    # -----------------------
    # FINAL COLUMNS
    # -----------------------
    final_columns = [
        "qid",
        "label",
        "gender",
        "citizenship",
        "citizenship_label",
        "pob_country",
        "place_of_birth_country_label",
        "place_of_birth_country_label_hdi",
        "unm49",
        "educated_at_label",
        "educated_at_country_label",
        "educated_at_country_label_hdi",
        "date_of_birth",
        "total_claims",
        "external_ids",
        "c_claims",
        "pareto_ext"
    ]

    df = df[[col for col in final_columns if col in df.columns]]

    # -----------------------
    # SAVE
    # -----------------------
    output_path = os.path.join(cat_path, f"/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Data/raw data/{cat_name}_final.csv")
    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")
    print(f"Entities: {len(df)}")


# -----------------------
# RUN
# -----------------------
def main():
    for category in os.listdir(BASE_DIR):
        print(category)
        cat_path = os.path.join(BASE_DIR, category)

        if os.path.isdir(cat_path):
            process_category(cat_path, category)


if __name__ == "__main__":
    main()