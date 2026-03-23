import pandas as pd
import requests
import time

df = pd.read_csv("/Users/liadraetta/Desktop/tutorial-experiment/pareto_entities_Directors.csv")

qids = df["QID"].tolist()

BATCH = 200
results = []

url = "https://query.wikidata.org/sparql"

headers = {
    "User-Agent": "ResearchBot/1.0",
    "Accept": "application/sparql-results+json"
}

for i in range(0, len(qids), BATCH):

    batch = qids[i:i+BATCH]
    values = " ".join([f"wd:{q}" for q in batch])

    query = f"""
    SELECT ?item ?genderLabel ?citizenshipLabel WHERE {{
      VALUES ?item {{ {values} }}
      OPTIONAL {{ ?item wdt:P21 ?gender }}
      OPTIONAL {{ ?item wdt:P27 ?citizenship }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    """

    r = requests.get(url, params={"query": query}, headers=headers)

    if r.status_code != 200:
        print("SPARQL error:", r.status_code)
        continue

    try:
        data = r.json()
    except:
        print("Invalid response, skipping batch")
        continue

    for b in data["results"]["bindings"]:

        qid = b["item"]["value"].split("/")[-1]

        gender = b.get("genderLabel", {}).get("value")
        citizenship = b.get("citizenshipLabel", {}).get("value")

        results.append({
            "QID": qid,
            "gender": gender,
            "citizenship": citizenship
        })

    print(f"Processed {i+len(batch)} / {len(qids)}")

    time.sleep(1)   # important: avoid rate limits

extra = pd.DataFrame(results)

df = df.merge(extra, on="QID", how="left")

df.to_csv("/Users/liadraetta/Desktop/tutorial-experiment/entities_enriched.csv", index=False)

print("Saved enriched dataset")