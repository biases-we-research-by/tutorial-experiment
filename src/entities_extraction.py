import requests
import json
import time
import os


SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
ENTITY_API = "https://www.wikidata.org/w/api.php"
HEADERS = {
    "Accept": "application/sparql-results+json",
}
OUTPUT_FILE = "../entities/directors.jsonl"
BATCH_SIZE = 50
MAX_RETRIES = 5
DELAY_BETWEEN_BATCHES = 0.2  # seconds
Qid = 'Q3455803'
# -----------------------------
# STEP 1 — Get 20k director QIDs
# -----------------------------
print("Querying SPARQL for 20,000 directors...")
query = f"""
SELECT ?person WHERE {{
  ?person wdt:P106 wd:{Qid} .
}}
LIMIT 20000
"""
response = requests.get(SPARQL_ENDPOINT, params={"query": query}, headers=HEADERS, timeout=60)
response.raise_for_status()
results = response.json()
qids = [r["person"]["value"].split("/")[-1] for r in results["results"]["bindings"]]
print(f"Collected {len(qids)} director QIDs.")



def robust_get(url, headers, max_retries=MAX_RETRIES):
    for attempt in range(max_retries):
        try:
            r = requests.get(url, headers=headers, timeout=60)
            r.raise_for_status()
            return r
        except (requests.ConnectionError, requests.Timeout) as e:
            wait = 2 ** attempt
            print(f"[Retry {attempt + 1}/{max_retries}] Error: {e}. Waiting {wait}s...")
            time.sleep(wait)
    raise Exception(f"Failed to download {url} after {max_retries} retries.")


# -----------------------------
# STEP 3 — Download entities in batches & convert
# -----------------------------
start_idx = 0
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r") as f:
        start_idx = sum(1 for _ in f) * BATCH_SIZE
    print(f"Resuming from batch index ~{start_idx}")

with open(OUTPUT_FILE, "a") as out_file:
    for i in range(start_idx, len(qids), BATCH_SIZE):
        batch_qids = qids[i:i + BATCH_SIZE]
        ids_str = "|".join(batch_qids)
        url = f"{ENTITY_API}?action=wbgetentities&ids={ids_str}&format=json"

        r = robust_get(url, HEADERS)
        data = r.json()

        for entity in data["entities"].values():
            # MediaWiki-like conversion
            mw_entity = {
                "pageid": entity.get("id", 0),  # use QID as pageid for simplicity
                "ns": 0,
                "title": entity.get("id", ""),
                "claims": entity.get("claims", {}),
                "labels": entity.get("labels", {}),
                "descriptions": entity.get("descriptions", {}),
            }
            out_file.write(json.dumps(mw_entity) + "\n")

        print(f"Downloaded and converted batch {i // BATCH_SIZE + 1} / {len(qids) // BATCH_SIZE}")
        time.sleep(DELAY_BETWEEN_BATCHES)

print(f"Done! Saved all MediaWiki-like director entities to {OUTPUT_FILE}")