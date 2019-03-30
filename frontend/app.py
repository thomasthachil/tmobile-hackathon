
from flask import Flask, render_template, request, jsonify
# from flask_wtf import FlaskForm
# from wtforms import IntegerField, validators, StringField
# from wtforms_components import TimeField

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
        radius = request.form['radius']
    return render_template('findReview.html')


@app.route('/find-customer', methods=['GET', 'POST'])
def findCustomer():
    if request.method == 'POST':
        zipcode = request.form['zipcode']
        radius = request.form['radius']

    return render_template('findCustomer.html')


@app.route('/review', methods=['GET'])
def review():

    store = 'atlanta-20'
    totalRating = 4.3
    totalSentiment = 0.556
    keyPhrases = {}
    keyPhrases['positive'] = ['excellent service',
                              'friendly people', 'wide selection']
    keyPhrases['negative'] = ['bad attitude', 'scam artist', 'unprofessional']
    reviews = {}
    positive = {}
    positive['atlanta-20'] = [3.3, 0.25, ['blah', 'blah2', 'blah3']]
    positive['atlanta-30'] = [2.3, 0.23, ['blah', 'blah2', 'blah3']]
    positive['atlanta-40'] = [1.3, 0.15, ['blah', 'blah2', 'blah3']]
    reviews['positive'] = {}

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
