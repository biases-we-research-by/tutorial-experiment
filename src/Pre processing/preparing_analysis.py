import os
import json
import pandas as pd
from src.utils.utils import unm49_mapping, generation_mapping, hdi_mapping

BASE_DIR = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Data/raw data"
OUTPUT_DIR = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Data/cleaned_data"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_label(labels, lang="en"):
    for l in labels:
        if l["language"] == lang:
            return l["value"]
    return None


def process_category(cat_path, cat_name):
    print(f"\nProcessing: {cat_name}")

    countries_path = os.path.join(cat_path, "countries.json")
    entity_json_path = os.path.join(cat_path, f"{cat_name}.json")
    pareto_path = os.path.join(cat_path, "pareto.csv")

    countries = load_json(countries_path)
    entities = load_json(entity_json_path)

# FILTER DATA Where "IsMain" == True (The target occupation is the first)
    entities = [e for e in entities if e.get("isMain") is True]

    # -----------------------
    # LABEL MAP (IMPORTANT FIX)
    # -----------------------
    label_map = {
        c["entity"]: extract_label(c["labels"])
        for c in countries
    }

    # -----------------------
    # BASE DF
    # -----------------------
    rows = []
    for e in entities:
        claims = e.get("entity_claims", {})

        def safe_first(d, key):
            values = d.get(key, [])
            return values[0] if values else None

        rows.append({
            "qid": e["entity"],
            "label": extract_label(e["labels"]),
            "date_of_birth": safe_first(claims, "P569"),
            "total_claims": e.get("total_claims"),
            "external_ids": e.get("external_ids")
        })

    df = pd.DataFrame(rows)

    # -----------------------
    # PARETO
    # -----------------------
    pareto = pd.read_csv(pareto_path)
    pareto["qid"] = pareto["entity"]
    pareto = pareto[["qid", "pareto_claims", "pareto_ext"]]

    df = df.merge(pareto, on="qid", how="left")

    # -----------------------
    # CITIZENSHIP
    # -----------------------
    cit_path = os.path.join(cat_path, "P27.csv")
    if os.path.exists(cit_path):
        cit = pd.read_csv(cit_path)
        if len(cit.columns) == 2:
            cit.columns = ["qid", "citizenship"]
        else:
            cit.columns = ["qid", "citizenship", "countryLabel", "continent", "unm49_mapping", "hdi"]
        df = df.merge(cit, on="qid", how="left")
        df["citizenship_label"] = df["citizenship"].map(label_map)

    # -----------------------
    # PLACE OF BIRTH
    # -----------------------
    pob_path = os.path.join(cat_path, "P19.csv")
    if os.path.exists(pob_path):
        pob = pd.read_csv(pob_path)

        pob = pob.rename(columns={
            "entity": "qid",
            "country": "birth_country"
        })

        pob["birth_country_label"] = pob["birth_country"].map(label_map)
        pob["birth_unm49"] = pob["birth_country_label"].map(unm49_mapping)
        pob["birth_hdi"] = pob["birth_country_label"].map(hdi_mapping)

        df = df.merge(
            pob[[
                "qid",
                "birth_country",
                "birth_country_label",
                "birth_hdi",
                "birth_unm49"
            ]],
            on="qid",
            how="left"
        )

    # -----------------------
    # EDUCATED AT (FIXED)
    # -----------------------
    edu_path = os.path.join(cat_path, "P69.csv")

    if os.path.exists(edu_path):
        edu = pd.read_csv(edu_path)

        edu = edu.rename(columns={
            "entity": "qid",
            "country": "edu_country",
            "P69": "educated_at"
        })

        edu["edu_country_label"] = edu["edu_country"].map(label_map)
        edu["edu_nm49"] = edu["edu_country_label"].map(unm49_mapping)
        edu["edu_hdi"] = edu["edu_country_label"].map(hdi_mapping)

        # SAFE LABEL MAPPING
        def safe_map(val):
            if pd.isna(val):
                return None
            return label_map.get(val, None)

        edu["educated_at_label"] = edu["educated_at"].apply(safe_map)

        df = df.merge(
            edu[[
                "qid",
                "educated_at",
                "educated_at_label",
                "edu_country",
                "edu_country_label",
                "edu_nm49",
                "edu_hdi",
            ]],
            on="qid",
            how="left"
        )

        df["edu_mobility"] = (
                (df["edu_country"].notna()) &
                (df["birth_country"].notna()) &
                (df["edu_country"] != df["birth_country"])
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
        }

        gender["gender"] = gender["gender_qid"].map(gender_map)
        gender = gender[["qid", "gender"]]

        df = df.merge(gender, on="qid", how="left")

    # -----------------------
    # GENERATION
    # -----------------------
    df["generation"] = df["date_of_birth"].map(generation_mapping)

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
    # FINAL COLUMNS (UPDATED)
    # -----------------------
    final_columns = [
        "qid",
        "label",
        "gender",
        "citizenship",
        "citizenship_label",
        "birth_country",
        "birth_country_label",
        "birth_hdi",
        "birth_unm49",
        "educated_at",
        "educated_at_label",
        "edu_country",
        "edu_country_label",
        "edu_hdi",
        "edu_nm49",
        "edu_mobility",
        "date_of_birth",
        "generation",
        "total_claims",
        "external_ids",
        "pareto_ext",
        "pareto_claims"
    ]

    df = df[[col for col in final_columns if col in df.columns]]

    # -----------------------
    # SAVE
    # -----------------------
    output_path = os.path.join(OUTPUT_DIR, f"{cat_name}.csv")
    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")
    print(f"Entities: {len(df)}")


def main():
    already_processed = {
        os.path.splitext(f)[0]
        for f in os.listdir(OUTPUT_DIR)
        if f.endswith(".csv")
    }

    for category in os.listdir(BASE_DIR):
        cat_path = os.path.join(BASE_DIR, category)

        if not os.path.isdir(cat_path):
            continue

        if category in already_processed:
            print(f"Skipping {category}")
            continue

        process_category(cat_path, category)


if __name__ == "__main__":
    main()