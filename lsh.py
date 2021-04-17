from __future__ import division
import pandas as pd
import numpy as np
import sys
import random

class LSH():

    def __init__(self, n_features, n_minhash=20):
        a_hash = [np.array([np.random.uniform(0,1) for _ in range(n_features)]) for _ in range(n_minhash)]
        b_hash = [random.uniform(0,1) for _ in range(n_minhash)]
        self.n_features = n_features
        self.n_minhash = n_minhash
        self.seeds = zip(a_hash, b_hash)
        self.df = pd.DataFrame(columns=['title'] + ['minhash_{}'.format(i + 1) for i in range(n_minhash)])

    def insert_document(self, title, s_doc):

        v_doc = np.array([np.float(i) for i in filter(None,
            s_doc.split(' '))])
        if v_doc.size != self.n_features:
            raise ValueError("Expected size {}".format(self.n_features))
        index = len(self.df)
        #values = [title] + [np.dot(a, v_doc) + b for a, b in self.seeds]
        values = [title] + [int(np.dot(a, v_doc) + b) for a, b in self.seeds]
        self.df.loc[index] = values
        return index

    def get_similarities(self):
        n_docs = len(self.df['title'])
        result = pd.DataFrame(columns=['title']+self.df['title'].values.tolist())
        for actual_doc in range(n_docs):
            title_actual = self.df.loc[actual_doc]['title']
            v_actual = self.df.loc[actual_doc][1:]
            result.loc[actual_doc] = [title_actual] + [np.sum(v_actual == self.df.loc[doc2][1:]) / self.n_minhash for doc2 in range(n_docs)]
        with pd.ExcelWriter('output.xlsx') as writer:
            result.to_excel(writer,sheet_name='sheet1')
        return result

    def closest_match(self, title):

        pd_df = self.get_similarities()
        return pd_df[pd_df['title'] == title]

