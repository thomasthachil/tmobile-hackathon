from flask import Flask, render_template, request, jsonify
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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasupersecretkey!'
subscription_key = os.environ['MS_KEY']
assert subscription_key
text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
df = pd.read_json('../datascraper/data.json')

# TODO: Have each method be self contained, calling only the other methods it needs.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/review')
def review():
    return render_template('review.html')


@app.route('/_storeRating')
def storeRating():
    store = request.args.get('store', 't-mobile-atlanta-13', type=str)
    global df
    revoi = df.loc[df['name'] == store]['reviews'].values[0]
    idnum = 1
    docDic = []
    ratings = []
    for rev in revoi:
        # docDic.append({'id':idnum, 'language':'en', 'text': rev[0]})
        ratings.append(rev[1])
        # idnum += 1
    return jsonify(rating=(sum(ratings) / float(len(ratings))))

    

    
