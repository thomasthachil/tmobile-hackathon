
from flask import jsonify
from bokeh.resources import CDN
from bokeh.embed import json_item
import json
from flask import Flask, render_template, request

from model import *
from graphics import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasupersecretkey!'
db = StoreDB()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/find-review', methods=['GET', 'POST'])
def findReview():
    if request.method == 'POST':
        zipcode = request.form['zipcode']
        # get results from the model

        # find all stores that have this sizpcode
        results = db.zipcode_lookup(zipcode)
        # result1 = {}
        # result2 = {}
        # result3 = {}
        # result1['store'] = 'atlanta-20'
        # result1['totalRating'] = 4.3
        # result1['totalSentiment'] = 0.556
        # result2['store'] = 'atlanta-20'
        # result2['totalRating'] = 1.3
        # result2['totalSentiment'] = 0.156
        # result3['store'] = 'atlanta-30'
        # result3['totalRating'] = 2.3
        # result3['totalSentiment'] = 0.356
        # results = [result1, result2, result3]
        return render_template('findReview.html', results=results)

    return render_template('findReview.html')


@app.route('/find-customer', methods=['GET', 'POST'])
def findCustomer():
    if request.method == 'POST':
        name = request.form['associate']
        timeTil = request.form['time']
        print(name)
        print(timeTil)

    return render_template('customer.html', results=True)

@app.route('/review/<store>', methods=['GET'])
def review(store):
    store = store
    totalRating = 4.3
    totalSentiment = 0.556
    keyPhrases = {}
    pos = []
    neg = []
    for doc in db.key_phrases_pos(store):
        pos += doc['keyPhrases']
    for doc in db.key_phrases_neg(store):
        neg += doc['keyPhrases']
    keyPhrases['positive'] = [str(r) for r in pos]
    keyPhrases['negative'] = [str(r) for r in neg]

    raw_revs = db.get_raw_reviews(store)
    reviews = {}
    positive = []
    negative = []
    print(len(raw_revs[0]))
    for i in range(len(raw_revs)):
        print(raw_revs[8][1])
        positive.append([raw_revs[i][1], db.get_indexed_sent(store, i), db.get_indexed_pos_keyPhrases(store,i), raw_revs[i][0], raw_revs[i][2]])
        negative.append([raw_revs[i][1], db.get_indexed_sent(store, i), db.get_indexed_neg_keyPhrases(store,i), raw_revs[i][0], raw_revs[i][2]])

    # positive.append([3.3, 0.25, ['blah', 'blah2', 'blah3']])
    # positive.append([2.3, 0.23, ['blah', 'blah2', 'blah3']])
    # positive.append([1.3, 0.15, ['blah', 'blah2', 'blah3']])
    reviews['positive'] = positive
    reviews['negative'] = negative

    return render_template('reviewGraph.html', store=store, totalRating=totalRating,
                           totalSentiment=totalSentiment, keyPhrases=keyPhrases,
                           reviews=reviews)


@app.route('/_storeRating')
def storeRating():
    store = request.args.get('store', 't-mobile-atlanta-13', type=str)
    global df
    revoi = df.loc[df['name'] == store]['reviews'].values[0]
    idnum = 1
    docDic = []
    ratings = []

    # rev 0 is review
    # rev1 is score otu of 5
    #rev2 is date

    for rev in revoi:
        # docDic.append({'id':idnum, 'language':'en', 'text': rev[0]})
        ratings.append(rev[1])
        # idnum += 1
    return jsonify(rating=(sum(ratings) / float(len(ratings))))


@app.route('/getStoreReviewHistory', methods = ['GET'])
def history():
    store = request.args.get('store', 't-mobile-atlanta-13', type=str)
    plotter = ChefJeff(db, store)

    return json.dumps(json_item(plotter.getReviewsOverTime(), "overtime"))

@app.route('/getDevices', methods = ['GET'])
def devices():
    store = request.args.get('store', 't-mobile-atlanta-13', type=str)
    plotter = ChefJeff(db, store)

    return json.dumps(json_item(plotter.getPhoneChart(), "devices"))

@app.route('/getServiceRatings', methods = ['GET'])
def ratings():
    store = request.args.get('store', 't-mobile-atlanta-13', type=str)
    plotter = ChefJeff(db, store)

    return json.dumps(json_item(plotter.getServiceSentimentChart(), "service"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 5000, debug = True)

