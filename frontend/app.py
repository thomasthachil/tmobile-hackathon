
from flask import Flask, render_template, request, jsonify
from model import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasupersecretkey!'


# TODO: Have each method be self contained, calling only the other methods it needs.


# class HealthForm(FlaskForm):
#     zipcode = IntegerField('Zip Code', validators=[
#                            validators.input_required(), validators.Length(min=5, max=5)])
#     radius = IntegerField('Radius', validators=[validators.input_required()])


# class MeetingForm(FlaskForm):
#     customerName = StringField('Customer Name', validators=[
#                                validators.input_required()])
#     time = TimeField('Appointment Time', validators=[
#                      validators.input_required()])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/find-review', methods=['GET', 'POST'])
def findReview():
    if request.method == 'POST':
        zipcode = request.form['zipcode']
        # get results from the model

        result1 = {}
        result2 = {}
        result3 = {}
        result1['store'] = 'atlanta-20'
        result1['totalRating'] = 4.3
        result1['totalSentiment'] = 0.556
        result2['store'] = 'atlanta-20'
        result2['totalRating'] = 1.3
        result2['totalSentiment'] = 0.156
        result3['store'] = 'atlanta-20'
        result3['totalRating'] = 2.3
        result3['totalSentiment'] = 0.356
        results = [result1, result2, result3]
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


@app.route('/review', methods=['GET'])
def review():

    # if request.method == ['GET']:
    #     request.store
    # db = StoreDB()

    store = 'atlanta-20'
    totalRating = 4.3
    totalSentiment = 0.556
    keyPhrases = {}
    keyPhrases['positive'] = ['excellent service',
                              'friendly people', 'wide selection']
    keyPhrases['negative'] = ['bad attitude', 'scam artist', 'unprofessional']
    reviews = {}
    positive = []
    positive.append([3.3, 0.25, ['blah', 'blah2', 'blah3']])
    positive.append([2.3, 0.23, ['blah', 'blah2', 'blah3']])
    positive.append([1.3, 0.15, ['blah', 'blah2', 'blah3']])
    reviews['positive'] = positive

    return render_template('review.html', store=store, totalRating=totalRating, totalSentiment=totalSentiment, keyPhrases=keyPhrases, reviews=reviews)


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
