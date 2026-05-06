import requests
import json
import time
import os
from typing import Dict,List
import pandas as pd
from tqdm import tqdm
import logging as log
from datasets import load_dataset
import csv
from tqdm import tqdm

log.basicConfig(
    level=log.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S"
)

HEADERS = {
    "Accept": "application/sparql-results+json",
}


class WikidataExtractor:

    def __init__(self):
        self.sprql = "https://query.wikidata.org/sparql"
        self.wdapi = "https://www.wikidata.org/w/api.php"
        
        self.sparql_headers = {
            "User-Agent":"CallMyAgent/1.0",
            "Accept": "application/sparql-results+json"
            }

        self.api_headers = {
            "User-Agent":"MyApp/1.0 (marcoantonio.stranisci@unito.it)"
            }
        

    def extract_entities(self, prop:str, cl:str,limit=None,offset=0):
        if limit:
            query = f"""
                SELECT ?entity WHERE {{
                ?entity wdt:{prop} wd:{cl} .
                }}
                LIMIT {limit} OFFSET {offset}
                """
        else:
            query = f"""
                SELECT ?entity WHERE {{
                ?entity wdt:{prop} wd:{cl} .
                }}
                
                """

        try:
            response = requests.get(self.sprql, params={"query": query}, headers=self.sparql_headers, timeout=60)
            response.raise_for_status()
            results = response.json()
            qids = [r["entity"]["value"].split("/")[-1] for r in results["results"]["bindings"]]
            log.info(f"gathered {len(qids)} entities")
            return qids
            
        except Exception as e: 
            log.info(e)
            return None
    

    def _find_claims(self, entities: List[str], retries: int = 3, backoff: float = 1.5):
        
        wd_params = {
            'format': 'json',
            'action': 'wbgetentities',
            'ids': '|'.join(entities),
            'props': 'claims|labels|sitelinks'
        }

        attempt = 0
        while attempt < retries:
            try:
                response = requests.get(
                    self.wdapi,
                    params=wd_params,
                    headers=self.api_headers,
                    timeout=30
                )

                response.raise_for_status()  # catches HTTP errors (4xx, 5xx)

                return response.json()

            except (requests.RequestException, ValueError) as e:
                attempt += 1

                if attempt >= retries:
                    log.info(f"{getattr(response, 'status_code', 'N/A')}. Error: {e}. Returning None")
                    return None

                sleep_time = backoff ** attempt
                log.warning(f"Attempt {attempt} failed: {e}. Retrying in {sleep_time:.1f}s...")
                time.sleep(sleep_time)
    
    def _count_claims(self,entity_claims):
        i = 0
        j = 0

        for item in entity_claims:
            i+=len(entity_claims[item])

            for element in entity_claims[item]:
                if element['mainsnak']['datatype'] == 'external-id':
                    j+=1

        return i,j        

    def _get_claims(self,entity_claims:Dict,target_claims:List):

        tot_prop = [x for x in entity_claims]

        target_prop = [x for x in target_claims if x in tot_prop]

        claims = dict()

        for p in target_prop:
            props = list()
            for cl in entity_claims[p]:
                try:
                    claim = cl['mainsnak']['datavalue']['value']
                    if 'id' in claim:
                        props.append(claim['id'])
                    elif 'time' in claim:
                        props.append(claim['time'])
                    else:
                        props.append(claim)
                except Exception as e: log.info(f"Error: {e}")
            claims[p] = props
        
        return claims
    
    def _get_labels(self,entity_claims:Dict,langs:List[str]):
        labels = list()
        for lang in langs:
            try:
                if lang in entity_claims['labels']:
                    labels.append(entity_claims['labels'][lang])
                else:
                    labels.append({"language":lang,"value":None})
            except Exception as e:
                log.info(f"Error: {e}")
        
        return labels
    
    def _get_wpages(self,entity_claims:Dict,editions:List[str]):
        sites = list()
        for ed in editions:
            try:
                if ed in entity_claims['sitelinks']:
                    sites.append({'site': ed, 'title': entity_claims['sitelinks'][ed]['title']})
                    
                else:
                    sites.append({'site':ed,"title":None})
            except Exception as e:
                log.info(f"Error: {e}")
        
        return sites
    
    def save_file(self,data,path,format):
        if format == 'json':
            with open(path,'w') as f:
                json.dump(data,f)
        elif format == 'csv':
            pd.DataFrame(data).to_csv(path,index=False)
    
    

    def extract_all_entities(self,
                             ents:List[str],
                             target_claims:List[str],
                             langs:List[str]=['en'],
                             editions:List[str]=['enwiki'],
                             format:str=None,
                             path:str=None):
        
        size = 50
        entities = [ents[i:i + size] for i in range(0, len(ents), size)]
        extracted_entities = list()
        for ent_batch in tqdm(entities):
            tmp = list()
            ents = self._find_claims(ent_batch)
            if ents is not None:
                log.info(f"processing {len(ents['entities'])} entities")
                for ent in ents['entities']:
                    try:
                        d = dict()
                        d['entity'] = ent
                        all_claims = ents['entities'][ent]['claims']
                        tot,ext = self._count_claims(all_claims)
                        ent_claims = self._get_claims(all_claims,target_claims)

                        labels = self._get_labels(ents['entities'][ent],langs)
                        sites = self._get_wpages(ents['entities'][ent],editions)
                        
                        d['total_claims'] = tot
                        d['external_ids'] = ext
                        d['entity_claims'] = ent_claims
                        d['labels'] = labels
                        d['wpages'] = sites

                        log.info(f"finished processing entity {ent}. Appending...")
                        
                        tmp.append(d)
                    except Exception as e:
                        log.info(f"Error: {e}")
            extracted_entities.extend(tmp)

        if path:
            self.save_file(extracted_entities,path,format)
                
        return extracted_entities


class HuggingGatherer:

    def __init__(self):
        pass
    
    def gater_dataset(self, dataset, lang, titles_list, output_csv):
        ds = load_dataset(dataset, f"latest.{lang}", split="train", streaming=True)

        with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'text']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for entry in tqdm(ds):
                if entry['title'] in titles_list:
                    writer.writerow({'title': entry['title'], 'text': entry['text']})
                    log.info(f"found page: {entry['title']}")






