import json
import os
import nltk
from nltk import FreqDist
import pandas as pd
import matplotlib.pyplot as plt
import re
import requests
from pprint import pprint
import matplotlib.pyplot as plt
import seaborn as sns
import time

subscription_key = 'c1005ffa18cc42ddbf916d2483bb2dd2'  # os.environ['MS_KEY']
assert subscription_key
text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"

class StoreDB:
    def __init__(self):
        try:
            print("Found File")
            self.df = pd.read_json('fullformJSON.json')
            print(self.df)
        except:
            self.df = pd.read_json('../datascraper/data.json', dtype=object)
            self.df = self.df.set_index('name')
            self.df['agg_sent'] = 0.0
            self.df['stars'] = 0.0
            self.df['sentiments'] = None
            self.df['sentiments'] = self.df['sentiments'].astype(object)
            self.df['key_phrases_pos'] = None
            self.df['key_phrases_pos'] = self.df['key_phrases_pos'].astype(object)
            self.df['key_phrases_neg'] = None
            self.df['key_phrases_neg'] = self.df['key_phrases_neg'].astype(object)
            for index, row in self.df.iterrows():
                idnum = 0
                docDic = []
                fiveRate = []
                for rev in self.df.loc[index]['reviews']:
                    docDic.append({'id':idnum, 'language':'en', 'text': rev[0]})
                    fiveRate.append(float(rev[1]))
                    idnum += 1
                self.df.at[index, 'stars'] = sum(fiveRate) / float(len(fiveRate))
                documents = {'documents' : docDic}
                headers   = {'Ocp-Apim-Subscription-Key': subscription_key}
                sentiment_api_url = text_analytics_base_url + "sentiment"
                response  = requests.post(sentiment_api_url, headers=headers, json=documents)
                sentiments = response.json()
                sent_scores = []
                pos_docs = []
                neg_docs = []
                try:
                    for doc in sentiments['documents']:
                        val = doc['score']
                        if val > 0.5:
                            pos_docs.append(doc['id'])
                        else:
                            neg_docs.append(doc['id'])
                        sent_scores.append(doc['score'])
                except:
                    print(documents)
                    print(sentiments)
                self.df.at[index, 'agg_sent'] = sum(sent_scores) / float(len(sent_scores))
                self.df.at[index, 'sentiments'] = sentiments['documents']

                key_phrase_api_url = text_analytics_base_url + "keyPhrases"
                headers   = {'Ocp-Apim-Subscription-Key': subscription_key}
                response  = requests.post(key_phrase_api_url, headers=headers, json=documents)
                key_phrases = response.json()
                pos_phrases = []
                neg_phrases = []
                for doc in key_phrases['documents']:
                    if doc['id'] in pos_docs:
                        pos_phrases.append(doc)
                    elif doc['id'] in neg_docs:
                        neg_phrases.append(doc)

                self.df.at[index, 'key_phrases_pos'] = pos_phrases
                self.df.at[index, 'key_phrases_neg'] = neg_phrases
            
            self.df.to_json('fullformJSON.json')
            

    def key_phrases_pos(self, store):
        pos_phrases = self.df.loc[store]['key_phrases_pos']
        return pos_phrases
    
    def key_phrases_neg(self, store):
        neg_phrases = self.df.loc[store]['key_phrases_neg']
        return neg_phrases 

    def get_raw_reviews(self, store):
        raw_revs = self.df.loc[store]['reviews']
        return raw_revs

    def get_sentiments(self, store):
        return self.df.loc[store]['sentiments']

    def get_indexed_sent(self, store, id):
        sents = self.get_sentiments(store)
        for doc in sents:
            if doc['id'] == id:
                return doc['score']

    def get_avg_stars(self, store):
        return self.df.loc[store]['stars']

    def get_indexed_review(self, store, id):
        raw_rev = self.df.loc[store]['reviews'][id][0]
        return raw_rev

    def get_indexed_pos_keyPhrases(self, store, id):
        pos_phrase_all = self.key_phrases_pos(store)
        for doc in pos_phrase_all:
            if doc['id'] == id:
                return doc['keyPhrases']

    def get_indexed_neg_keyPhrases(self, store, id):
        neg_phrase_all = self.key_phrases_neg(store)
        for doc in neg_phrase_all:
            if doc['id'] == id:
                return doc['keyPhrases']

    def get_agg_sent(self, store):
        return self.df.loc[store]['agg_sent']

    def keyword_search(self, store, word):
        sentiments4word = []
        pos_phrases = self.key_phrases_pos(store)
        neg_phrases = self.key_phrases_neg(store)

        for doc in pos_phrases:
            if word in doc['keyPhrases']:
                sentiments4word.append(self.get_indexed_sent(store, doc['id']))
        
        return sentiments4word

    def get_zipcode(self, store):
        return self.df.loc[store]['location']['zip_code']
    
    def zipcode_lookup(self, zipcode):
        storesAndData = []
        for index, row in self.df.iterrows():
            if int(row.location['zip_code']) == int(zipcode):
                storesAndData.append({'name':index, 'rating':row.stars, 'sent':row.agg_sent, 'zipcode':int(zipcode)})
        return storesAndData





if __name__ == "__main__":
    DB = StoreDB()