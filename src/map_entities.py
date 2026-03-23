import glob
import regex as re
import pandas as pd
from utils.mapping import country_to_continent,cultural_mapping,map_labels,hdi_mapping


targetInfo = "Q6625963"

toMap = ['P19','P69','P108']

places = list()
for doc in glob.glob(f"output/{targetInfo}/*"):
    if re.search('|'.join(toMap),doc):
        df = pd.read_csv(doc)
        df['countryLabel'] = df.country.apply(lambda x:map_labels.get(x,None))
        print(df.dropna())
        df['continent'] = df.countryLabel.apply(lambda x:country_to_continent.get(x,{}))
        df['cultural'] = df.countryLabel.apply(lambda x:cultural_mapping.get(x,{}))
        df['hdi'] = df.countryLabel.apply(lambda x:hdi_mapping.get(x,{}))
        df.to_csv(doc,index=False)
