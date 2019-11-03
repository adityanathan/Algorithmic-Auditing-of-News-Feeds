import pickle
import gensim
import numpy as np

with open('batch_coherence.pkl', 'rb') as f:
    while True:
        try:
            # i, _, time_arr, _, _, _ = pickle.load(f)
            tup = pickle.load(f)
        except:
            break


# print('_______________-')
print(tup)
