import json,glob
import numpy as np
import pandas as pd
from tqdm import tqdm

PATH = 'data/generation output/*Mistral*.json'


def brier(preds):

    brier_score = [(1 - p) ** 2 if p >= 0.7 else (0-p) ** 2 for p in preds]

    return np.mean(brier_score)


l = list()
for doc in tqdm(glob.glob(PATH)):
    jsn = json.load(open(doc,'r'))
    for item in jsn:
        preds = [x['probability'] for x in item['token_details']]
        l.append({'entity':item['qid'],'brier_score':brier(preds)})

df = pd.DataFrame(l)

df["decile"] = pd.qcut(df["brier_score"], 10, labels=False)


df.to_csv('brier_scores_Mistral.csv',index=False)
'''



for doc in tqdm(glob.glob(PATH)):
    l = list()
    m = list()
    model = doc.split('/')[-1].split('_')[-1][:-5]
    group = doc.split('/')[-1].split('_')[0]
    jsn = json.load(open(doc,'r'))
    
    length = np.quantile([len(x['token_details']) for x in jsn],0.5)

    for i in range(int(round(length))):
        preds = [x['token_details'][i]['probability'] for x in jsn if len(x['token_details']) > i]
        preds_ = [x['token_details'][i]['probability'] for x in jsn if len(x['token_details']) > i and x['pareto_claims'] == 1]

        score = brier(preds)
        score_ = brier(preds_)


        l.append({'model':model,'group':group,'position':i,'brier_score':score})
        m.append({'model':model,'group':group,'position':i,'brier_score_':score_})
    df = pd.DataFrame(l)
    df_ = pd.DataFrame(m)
    n_slices = 10

    # Assign slice IDs
    df["slice"] = pd.cut(df.index, bins=n_slices, labels=False)
    df_["slice"] = pd.cut(df_.index, bins=n_slices, labels=False)

    # Replace values with slice mean
    df["value"] = df.groupby("slice")["brier_score"].transform("mean")
    df_["value"] = df_.groupby("slice")["brier_score_"].transform("mean")

    # Optional: drop helper column
    df = df.drop(columns="slice")
    df_ = df_.drop(columns="slice")

    
    df['head'] = df_['value']
    print(df['head'].drop_duplicates()- df['value'].drop_duplicates().to_list())
'''

'''with open('brier_scores.json','w') as f:
    json.dump(l,f)
        '''