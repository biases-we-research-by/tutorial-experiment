import os
import json
import pandas as pd
import ast
from mapping import unm49_mapping, generation_mapping, hdi_mapping, gender_mapping

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

        def safe_first(d, key):
            values = d.get(key, [])
            return values[0] if values else None

        claims = e.get("entity_claims", {})

        dob = safe_first(claims, "P569")
        rows.append({
            "qid": qid,
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
            cit.columns = ["qid", "citizenship","countryLabel","continent","unm49_mapping","hdi"]

        df = df.merge(cit, on="qid", how="left")
        df["citizenship_label"] = df["citizenship"].map(country_map)

    # -----------------------
    # PLACE OF BIRTH
    # -----------------------
    pob_path = os.path.join(cat_path, "P19.csv")
    if os.path.exists(pob_path):
        pob = pd.read_csv(pob_path)

        if "countryLabel" in pob.columns:
            pob = pob.rename(columns={"countryLabel": "birth_country_label"})
        if "hdi" in pob.columns:
            pob = pob.rename(columns={"hdi": "birth_hdi"})
        if "unm49_mapping" in pob.columns:
            pob = pob.rename(columns={"unm49_mapping": "birth_unm49"})
        pob = pob.rename(columns={
            "entity": "qid",
            "country": "birth_country",
        })

        if "birth_country_label" not in pob.columns:
            pob["birth_country_label"] = pob["birth_country"].map(country_map)
        if  "birth_unm49" not in pob.columns:
            pob["birth_unm49"] = pob["birth_country_label"].map(unm49_mapping)
        if  "birth_hdi" not in pob.columns:
            pob["birth_hdi"] = pob["birth_country_label"].map(hdi_mapping)

        if "birth_country_label" in pob.columns and "birth_hdi" in pob.columns and "birth_unm49" in pob.columns:
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
        else:
            df = df.merge(
                pob[[
                    "qid",
                    "birth_country",
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
        print("1", edu.columns)
        if "countryLabel" in edu.columns:
            edu = edu.rename(columns={"countryLabel": "edu_country_label"})
        if "hdi" in edu.columns:
            edu = edu.rename(columns={"hdi": "edu_hdi"})
        if "unm49_mapping" in edu.columns:
            edu = edu.rename(columns={"unm49_mapping": "edu_unm49"})
        edu = edu.rename(columns={
            "entity": "qid",
            "country": "edu_country",
        })
        print("2", edu.columns)
        if "edu_country_label" not in edu.columns:
            edu["edu_country_label"] = edu["edu_country"].map(country_map)
        print("3", edu.columns)
        if  "edu_nm49" not in edu.columns:
            edu["edu_nm49"] = edu["edu_country_label"].map(unm49_mapping)
        print("4", edu.columns)
        if  "edu_hdi" not in edu.columns:
            edu["edu_hdi"] = edu["edu_country_label"].map(hdi_mapping)
        print("5", edu.columns)


        if "edu_country_label" in edu.columns or "edu_hdi" in edu.columns or "edu_nm49" in edu.columns:
            df = df.merge(
                edu[[
                    "qid",
                    "edu_country",
                    "edu_country_label",
                    "edu_nm49",
                    "edu_hdi",
                ]],
                on="qid",
                how="left"
            )
        else:
            df = df.merge(
                edu[[
                    "qid",
                    "edu_country",
                ]],
                on="qid",
                how="left"
            )
        print("6", df.columns)

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
            "Q48270": "genderQueer",
            "Q121307094": "genderQueer",
            "Q2449503": "genderQueer",
            "Q1052281": "genderQueer",
            "Q189125": "genderQueer",
            "Q138806924": "genderQueer"
        }

        gender["gender"] = gender["gender_qid"].map(gender_map)
        gender = gender[["qid", "gender"]]

        df = df.merge(gender, on="qid", how="left")

    # -----------------------
    # UNM49 MAPPING
    # -----------------------
    #if "birth_country_label" in df.columns:
        #df["birth_unm49"] = df["birth_country_label"].map(unm49_mapping)

    #if "educated_at_country_label" in df.columns:
        #df["edu_unm49"] = df["educated_at_country_label"].map(unm49_mapping)

    if "date_of_birth" in df.columns:
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
    # FINAL COLUMNS
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
        "edu_country",
        "edu_country_label",
        "edu_hdi",
        "edu_nm49",
        "date_of_birth",
        "generation",
        "total_claims",
        "external_ids",
        "c_claims",
        "pareto_ext",
        "pareto_claims"
    ]



    df = df[[col for col in final_columns if col in df.columns]]

    # -----------------------
    # SAVE
    # -----------------------
    output_path = os.path.join(cat_path, f"/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Data/cleaned_data/{cat_name}.csv")
    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")
    print(f"Entities: {len(df)}")


# -----------------------
# RUN
# -----------------------
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
            print(f"Skipping category '{category}': file CSV già esistente.")
            continue
        print(f"Processing folder: {category}...")

        cat_path = os.path.join(BASE_DIR, category)
        if os.path.isdir(cat_path):
            process_category(cat_path, category)


if __name__ == "__main__":
    main()