

from flask import Flask, render_template, request, redirect, flash, session, url_for, jsonify
import os 
import pymongo

app = Flask(__name__)

app.secret_key = '5U\x9fa\xbb0w\xe3^*\xb2_\x02\x82H\rY\xcb\xc6\xa8.\xe7\xaa\xd8\x8f\xe4\xb70l0(\x12\xe259P\xef\xeb\xb7v\xecH\x08m,\x81\xd4\xf4'


if os.environ['MONGOHQ_URL']:
    try:
        print "Attempting MongoDB connection"
        db = pymongo.MongoClient(os.environ['MONGOHQ_URL']).get_default_database()
        print db, "success?"
    except:
        db = None


@app.route("/")
def index():
    return render_template('milklab-signin.html')


@app.route('/lab-dashboard')
def lab_dashboard():
    return render_template('dashboard.html')


@app.route("/milkdata", methods=['GET'])
def milkdata_dump():
    if request.method == 'GET':
        if db:
            return jsonify(db.milkdata.find())


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



@app.route('/login', methods=['GET', 'POST'])
def login():
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
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)