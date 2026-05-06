from extractor import HuggingGatherer
import pandas as pd

hg = HuggingGatherer()

ds_name = 'omarkamali/wikipedia-monthly'

names = pd.read_csv('output/wpages.csv').title.to_list()
hg.gater_dataset(dataset=ds_name,lang='en',titles_list=names,output_csv='output/enpages.csv')