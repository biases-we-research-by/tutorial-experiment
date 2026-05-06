from typing import List
import numpy as np
from scipy.spatial.distance import jensenshannon
from collections import Counter



class Labeler:
    def __init__(self):
        pass

    def pareto_threshold(self,values:List[int], threshold:float=0.8):
        vals = sorted(values, reverse=True)
        total = sum(vals)
        
        cum = 0
        for v in vals:
            cum += v
            if cum / total >= threshold:
                return v
    
    def _remove_low_frequent(self,words):
        counted = Counter(words)
        threshold = np.percentile(list(counted.values()), 5)
        filtered = [e for e in words if counted[e] > threshold]  

        return filtered 
    
    def js_divergence(self,p,q):

        p = self._remove_low_frequent(p)
        q = self._remove_low_frequent(q)
        count1 = Counter(p)
        count2 = Counter(q)

        all_words = set(p) | set(q)

        total1 = sum(count1.values())
        total2 = sum(count2.values())

        js_dict = {}

        for word in all_words:
            # Frequency of word in each list
            f1 = count1.get(word, 0) / total1
            f2 = count2.get(word, 0) / total2
            
            # Jensen-Shannon divergence (scipy returns sqrt of divergence by default)
            js_distance = jensenshannon([f1, 1-f1], [f2, 1-f2], base=2)
            direction = f1 - f2  # signed difference

            js_dict[word] = js_distance * (1 if direction >= 0 else -1)

        return js_dict
            
