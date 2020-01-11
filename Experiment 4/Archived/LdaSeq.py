#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
import numpy as np
import pickle
import re
import timeit
import spacy

import gensim
import gensim.corpora as corpora
from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess
from gensim.models import LdaMulticore, ldaseqmodel
from nltk.corpus import stopwords
from gensim.matutils import hellinger
import helper as he
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# In[ ]:


# # loading our corpus and dictionary
# try:
#     dictionary = Dictionary.load('datasets/news_dictionary')
# except FileNotFoundError as e:
#     raise ValueError("SKIP: Please download the Corpus/news_dictionary dataset.")
# corpus = bleicorpus.BleiCorpus('datasets/news_corpus')
# # it's very important that your corpus is saved in order of your time-slices!

# time_slice = [438, 430, 456]


# In[2]:


with open('../data/preprocessed_data/aadhar_corp.pkl','rb') as f:
    data_lemmatized, id2word, corpus = pickle.load(f)
    
with open('../data/massmedia-data/aadhar_date_indexed.pkl','rb') as f:
    _, time_index_arr = pickle.load(f)


# In[3]:


def generate_timeslice_data(index_arr):
    arr = []
    for i in index_arr.values():
        arr.append(i)
        
    diff_arr=[]
    for i in range(1,len(arr)):
        diff_arr.append(arr[i]-arr[i-1])
    return diff_arr


# In[4]:


time_slices = generate_timeslice_data(time_index_arr)


# In[ ]:


ldaseq = ldaseqmodel.LdaSeqModel(corpus=corpus, id2word=id2word, time_slice=time_slices, num_topics=35)


# In[ ]:




