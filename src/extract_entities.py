from extractor import WikidataExtractor
from labeler import Pareto

wd = WikidataExtractor()
lab = Pareto()
ents = wd.extract_entities(prop='P106',cl='Q6625963')

size = 50
entities = [ents[i:i + size] for i in range(0, len(ents), size)][0]

myentities = wd.get_claims(ents=entities,target_claims=['P19','P21','P27','P69','P108','P106','P569'],langs=['en','es','it'],editions=['enwiki','eswiki','itwiki'])

claims = [x['total_claims'] for x in myentities]
ext_ids = [x['external_ids'] for x in myentities]

thr_cl = lab.pareto_threshold(claims)
thr_ext = lab.pareto_threshold(ext_ids)

for myent in myentities:
    if myent['total_claims']>thr_cl:
        myent['pareto_claims'] = 'head'
    else:
        myent['pareto_claims'] = 'long'

    if myent['external_ids']>thr_ext:
        myent['pareto_ext'] = 'head'
    else:
        myent['pareto_ext'] = 'long'

print(myentities[0])

