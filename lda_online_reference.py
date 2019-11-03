import pandas as pd
import numpy as np
import pickle
import re
import timeit
import spacy

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel, HdpModel, LdaModel, LdaMulticore
from nltk.corpus import stopwords
import helper as he

'''
This is intended as a reference on how to train an online lda model
'''

with open('corp.pkl', 'rb') as f:
    data_lemmatized, id2word, corpus = pickle.load(f)

print(len(data_lemmatized))

print('Building Model')
start = timeit.default_timer()

lda = LdaMulticore(corpus, num_topics=35, id2word=id2word,
                   workers=3, chunksize=2000, passes=10, batch=False)

end = timeit.default_timer()
time_taken = end - start

coherencemodel2 = CoherenceModel(
    model=lda, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
print(coherencemodel2.get_coherence())

print('Time taken:'+str(end-start))
