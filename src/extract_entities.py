from extractor import WikidataExtractor
from labeler import Labeler
import json
import argparse
import logging as log
from tqdm import tqdm
from time import sleep
import pandas as pd
import glob
import regex as re
import os
from utils.mapping import country_to_continent,cultural_mapping,country_labels,hdi_mapping


targetInfo = "Q6625963"
'''
os.mkdir(f"output/{targetInfo}")

myfile = f'output/{targetInfo}.json'

log.basicConfig(
    level=log.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S"
)


wd = WikidataExtractor()
lab = Labeler()

#jsn = json.load(open(myfile))

props = ['P19','P21','P27','P69','P108','P106','P569']

people = wd.extract_entities(
    'P106',
    'Q6625963',
    limit=5_000
)

myentities = wd.extract_all_entities(
    ents=people,
    target_claims=props,
    langs = ['en','es','it'],
    editions=['enwiki','eswiki','itwiki'],
    path=myfile,
    format='json'
)

claims = [x['total_claims'] for x in myentities]
ext_ids = [x['external_ids'] for x in myentities]

thr_cl = lab.pareto_threshold(claims)
thr_ext = lab.pareto_threshold(ext_ids)


pareto = list()
for myent in myentities:
    d = dict()
    d['entity'] = myent
    if myent['total_claims']>thr_cl:
        d['pareto_claims'] = 'head'
        
    else:
        d['pareto_claims'] = 'head'

    if myent['external_ids']>thr_ext:
        d['pareto_ext'] = 'head'
    else:
        d['pareto_ext'] = 'long'

    pareto.append(d)

pd.DataFrame(pareto).to_csv(f"output/{targetInfo}/pareto.csv",index=False)


for item in props:
    myprop = list()
    for j in myentities:
        try:
            myprop.append({
                'entity':j['entity'],
                item:j['entity_claims'][item]
            })
        except Exception as e:
            print(e)
            myprop.append({
                'entity':j['entity'],
                item:None
            })
    pd.DataFrame(myprop).explode(column=item).to_csv(f"output/{targetInfo}/{item}.csv",index=False)
       

toMap = ['P19','P69','P108']

places = list()
for doc in glob.glob(f"output/{targetInfo}/*"):
    if re.search('|'.join(toMap),doc):
        df = pd.read_csv(doc).dropna()
        places.extend(df[list(df)[-1]].drop_duplicates())

places = list(set(places))

entsCountries = wd.extract_all_entities(
    ents=places,
    target_claims=['P17'],
    langs = ['en','es','it'],
    editions=['enwiki','eswiki','itwiki'],
    path=f"output/{targetInfo}/countries.json",
    format='json'
)



places = list()
for item in entsCountries:
    try:
        ent = item['entity']
        country = item['entity_claims']['P17']
        places.append({
            'temp_id':ent,
            'country':country
        })
    except: continue
countries = pd.DataFrame(places).explode('country')

for doc in glob.glob(f"output/{targetInfo}/*"):
    if re.search('|'.join(toMap),doc):
        df = pd.read_csv(doc).dropna()
        df = df.merge(countries,left_on=list(df)[-1],right_on='temp_id')
        df = df.drop(columns=['temp_id'])
        df.to_csv(doc,index=False)

'''


toMap = ['P19','P69','P108']

places = list()
for doc in glob.glob(f"output/{targetInfo}/*.csv"):
    if re.search('|'.join(toMap),doc):
        df = pd.read_csv(doc)

        
