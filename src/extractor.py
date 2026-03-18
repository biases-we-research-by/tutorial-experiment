import requests
import json
import time
import os
from typing import Dict,List

import logging as log

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
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        

    def extract_entities(self, prop:str, cl:str,limit=20_000,offset=0):
        query = f"""
            SELECT ?entity WHERE {{
            ?entity wdt:{prop} wd:{cl} .
            }}
            LIMIT {limit} OFFSET {offset}
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
    
    def _find_claims(self,entities:List[str]):
        
        wd_params =  {
            'format':'json',
            'action':'wbgetentities',
            'ids':'{}'.format('|'.join(entities)),
            'props':'claims|labels|sitelinks'}
        
        response = requests.get(self.wdapi,params=wd_params,headers=self.api_headers,timeout=30)

        try:
            result = response.json()
            return result
        except Exception as e:
            log.info("Error: {e}. Returning None")
            return None
    
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
                claim = cl['mainsnak']['datavalue']['value']
                if 'id' in claim:
                    props.append(claim['id'])
                elif 'time' in claim:
                    props.append(claim['time'])
                else:
                    props.append(claim.keys())
            claims[p] = props
        
        return claims
    
    def _get_labels(self,entity_claims:Dict,langs:List[str]):
        labels = list()
        for lang in langs:
            if lang in entity_claims['labels']:
                labels.append(entity_claims['labels'][lang])
            else:
                labels.append({"language":lang,"value":None})
        
        return labels
    
    def _get_wpages(self,entity_claims:Dict,editions:List[str]):
        sites = list()
        print(entity_claims.keys())
        for ed in editions:
            if ed in entity_claims['sitelinks']:
                sites.append({'site': ed, 'title': entity_claims['sitelinks'][ed]['title']})
                
            else:
                sites.append({'site':ed,"title":None})
        
        return sites
    
    

    def get_claims(self,ents:List[str],target_claims:List[str],langs:List[str]=['en'],editions:List[str]=['enwiki']):

        my_entities = list()
        entities = self._find_claims(ents)
        print(entities.keys())
        if entities is not None:
            log.info(f"processing {len(entities['entities'])} entities")
            for ent in entities['entities']:
                d = dict()
                d['entity'] = ent
                all_claims = entities['entities'][ent]['claims']
                tot,ext = self._count_claims(all_claims)
                ent_claims = self._get_claims(all_claims,target_claims)

                labels = self._get_labels(entities['entities'][ent],langs)
                sites = self._get_wpages(entities['entities'][ent],editions)
                
                d['total_claims'] = tot
                d['external_ids'] = ext
                d['entity_claims'] = ent_claims
                d['labels'] = labels
                d['wpages'] = sites

                log.info(f"finished processing entity {ent}. Appending...")
                
                my_entities.append(d)
                

        

        return my_entities




