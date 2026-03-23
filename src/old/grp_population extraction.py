import pandas as pd
import requests
import warnings
from urllib3.exceptions import NotOpenSSLWarning
warnings.simplefilter("ignore", NotOpenSSLWarning)

df = pd.read_csv("/Models.csv")  # Replace with your CSV path

# GRP and population extractio
def get_qid(country):
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "search": country
    }
    headers = {
        "User-Agent": "MyWikidataScript/1.0 lia.draetta@unito.it"
    }
    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        if "search" in data and data["search"]:
            return data["search"][0]["id"]
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {country}: {e}")
    except ValueError:
        print(f"Invalid JSON response for {country}: {r.text[:100]}")
    return None

# ------------------------------
# Resolve Q-IDs for all unique countries
# ------------------------------
countries = df["citizenship"].unique().tolist()
country_qids = {c: get_qid(c) for c in countries}
print("Country Q-IDs:", country_qids)

# Filter out countries that couldn't be resolved
valid_qids = [qid for qid in country_qids.values() if qid is not None]

if not valid_qids:
    raise ValueError("No valid country Q-IDs found. Check your CSV or API requests.")

# ------------------------------
# Prepare SPARQL query
# ------------------------------
qid_values = " ".join(f"wd:{qid}" for qid in valid_qids)
sparql = f"""
SELECT ?country ?countryLabel ?population ?gdpNominal WHERE {{
  VALUES ?country {{ {qid_values} }}
  OPTIONAL {{ ?country wdt:P1082 ?population. }}
  OPTIONAL {{ ?country wdt:P2131 ?gdpNominal. }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
}}
"""

# ------------------------------
# Send SPARQL request
# ------------------------------
url = "https://query.wikidata.org/sparql"
headers = {
    "Accept": "application/sparql-results+json",
    "User-Agent": "MyWikidataScript/1.0 (your_email@example.com)"
}

try:
    r = requests.get(url, params={"query": sparql}, headers=headers, timeout=30)
    r.raise_for_status()
    res = r.json()
except requests.exceptions.RequestException as e:
    print("SPARQL request failed:", e)
    res = None
except ValueError:
    print("Invalid JSON response:", r.text[:200])
    res = None

if res is None:
    raise RuntimeError("Failed to get data from Wikidata SPARQL endpoint.")

# ------------------------------
# Parse results
# ------------------------------
country_data = {}
for item in res["results"]["bindings"]:
    qid = item["country"]["value"].split("/")[-1]
    population = int(item.get("population", {}).get("value", "0"))
    gdp = float(item.get("gdpNominal", {}).get("value", "0"))
    country_data[qid] = {"population": population, "gdpNominal": gdp}

# ------------------------------
# Map results back to CSV
# ------------------------------
df["countryQID"] = df["citizenship"].map(country_qids)
df["population"] = df["countryQID"].map(lambda q: country_data.get(q, {}).get("population"))
df["gdpNominal"] = df["countryQID"].map(lambda q: country_data.get(q, {}).get("gdpNominal"))

# ------------------------------
# Save new CSV
# ------------------------------
df.to_csv("/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/models_with_country_data.csv", index=False)
print("✅ CSV written with population & GDP!")