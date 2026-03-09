import json
import pandas as pd
import numpy as np

input_file = "/Users/liadraetta/Desktop/progetti/Projects/longTail-verbalization/OUTPUT/wikidata/wikidata_sample/all/Model.jsonl"
output_file = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/pareto_entities_Model.csv"
threshold = 0.8

rows = []

# -------------------------
# Step 1 — read JSONL file
# -------------------------
with open(input_file) as f:
    for line in f:
        e = json.loads(line)

        qid = e.get("title")

        # extract labels
        labels = e.get("labels", {})
        label_en = labels.get("en", {}).get("value")
        label_es = labels.get("es", {}).get("value")
        label_it = labels.get("it", {}).get("value")

        # count claims
        claims = e.get("claims", {})
        claim_count = sum(len(v) for v in claims.values())

        rows.append({
            "QID": qid,
            "label_en": label_en,
            "label_es": label_es,
            "label_it": label_it,
            "claims": claim_count
        })

# -------------------------
# Step 2 — create dataframe
# -------------------------
df = pd.DataFrame(rows)

# -------------------------
# Step 3 — Pareto cutoff
# -------------------------
df = df.sort_values("claims", ascending=False)

total_claims = df["claims"].sum()

df["cum_share"] = df["claims"].cumsum() / total_claims

cutoff_idx = np.argmax(df["cum_share"].values >= threshold)

cutoff_value = df.iloc[cutoff_idx]["claims"]

# -------------------------
# Step 4 — classify entities
# -------------------------
df["pareto_cutoff"] = cutoff_value

df["type"] = np.where(df["claims"] >= cutoff_value,
                      "Head",
                      "Long-tail")

# -------------------------
# Step 5 — save CSV
# -------------------------
df = df[[
    "QID",
    "label_en",
    "label_es",
    "label_it",
    "claims",
    "pareto_cutoff",
    "type"
]]

df.to_csv(output_file, index=False)

print("Pareto cutoff:", cutoff_value)
print("Saved to:", output_file)