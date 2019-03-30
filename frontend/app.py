from flask import Flask, render_template, request
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasupersecretkey!'

# TODO: Have each method be self contained, calling only the other methods it needs.

@app.route('/')
def index():
    return render_template('index.html')
