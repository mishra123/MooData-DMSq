

from flask import Flask, render_template, request, redirect, flash, session, url_for, jsonify, make_response
import os 
import json
from bson.json_util import dumps
from flask.ext.pymongo import PyMongo

app = Flask(__name__)



app.secret_key = '5U\x9fa\xbb0w\xe3^*\xb2_\x02\x82H\rY\xcb\xc6\xa8.\xe7\xaa\xd8\x8f\xe4\xb70l0(\x12\xe259P\xef\xeb\xb7v\xecH\x08m,\x81\xd4\xf4'

if 'MONGOHQ_URL' in os.environ:
    app.config['MONGO_URI'] = os.environ['MONGOHQ_URL']
    mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template('milklab-signin.html')


@app.route('/lab-dashboard')
def lab_dashboard():
    return render_template('dashboard.html')

@app.route('/lab-archive')
def lab_archive():
    return render_template('archive.html')


@app.route("/milkdata", methods=['GET'])
def milkdata_dump():
    if request.method == 'GET':
        
        res = make_response(dumps(mongo.db.milkdata.find()))

        res.headers['Access-Control-Allow-Origin'] = '*'

        return res


@app.route('/lab_login', methods=['GET', 'POST'])
def lab_login():
    if request.method == 'POST':
        
        print request.form
        print session

        if all(x in request.form for x in ('username','pw')): 
            
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            flash('something went wrong with your submission')
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return redirect(url_for('dashboard'))



@app.route('/app_login', methods=['POST', 'OPTIONS'])
def login():

    print request

    res = make_response(dumps({ 'user':'Daniel', 'farmer_id':1 }))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Content-Type'] = 'application/json'
    return res

        

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    
    app.run(debug=True)