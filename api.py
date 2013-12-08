

from flask import Flask, render_template, request, redirect, flash, session, url_for, jsonify, make_response
import os 
import json
import pymongo
from bson.objectid import ObjectId
import md5
from bson.json_util import dumps
from flask.ext.pymongo import PyMongo
from flask.ext.cors import origin
# from flask.ext.


app = Flask(__name__)



app.secret_key = '5U\x9fa\xbb0w\xe3^*\xb2_\x02\x82H\rY\xcb\xc6\xa8.\xe7\xaa\xd8\x8f\xe4\xb70l0(\x12\xe259P\xef\xeb\xb7v\xecH\x08m,\x81\xd4\xf4'

if 'MONGOHQ_URL' in os.environ:
    app.config['MONGO_URI'] = os.environ['MONGOHQ_URL']
    mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template('milklab-signin.html')


@app.route("/add_lab_user")
def add_lab_user():

    if 'email' in request.args and 'password' in request.args:
        password = md5.new()
        password.update(request.args['password']+request.args['email'])


        mongo.db.lab_users.update(
            #Object to search by
            {'email':request.args['email']},
            #Object to update by
            { "$set" : {
                'email':request.args['email'],
                'password':password.hexdigest()
                }
            },
            True #for upserting (update or insert if doesn't exist)
        )

    return redirect('/')


@app.route('/lab-dashboard', methods=['GET', 'POST'])
def lab_dashboard():

    if request.method == 'GET':

        #Check if user is in the session by checking for this key
        if 'email' in session:

            logged_in_user = session['email']

            user = mongo.db.lab_users.find_one({'email':logged_in_user['email']})



            #Section for handling the 30 most recent reports
            recent_thirty_reports = mongo.db.milkdata.find(\
                {'lab_user':user['_id']})\
                .sort('Date',-1).limit(30)

            #Convert cursor into a list
            recent_thirty_reports = [x for x in recent_thirty_reports]    

            #Get a set of all the farmer ids in recent reports so we can get farmer data
            farmer_objectsids = {
                ObjectId(x['farmer_user']) for x in recent_thirty_reports
            }

            #Go through each farmer_id in the set, get the userdata for that farmer and 
            # swap out the id in 'farmer_user' with a dictionary of user data
            for farmer_id in farmer_objectsids:
                
                f = mongo.db.users.find_one({"_id":farmer_id})
                #Maybe an incorrect farmer_id?
                if f:
                    #Go through all the reports and swap out ObjectId for actual farmer data
                    # This is basically a table join in MongoDB
                    for r in recent_thirty_reports:
                        if r['farmer_user'] == farmer_id:
                            r['farmer_user'] = f

            return render_template('dashboard.html', 
                user=logged_in_user, 
                recent_thirty_reports = recent_thirty_reports
                )    
        elif request.method == 'POST':
            #CODE HERE FOR HANDLING FORM INPUT

    else:
        return redirect(url_for('index'))
    

@app.route('/lab-archive')
def lab_archive():
    return render_template('archive.html')


@app.route("/milkdata", methods=['GET'])
@origin('*', headers='Content-Type')
def milkdata_dump():
    if request.method == 'GET':
        
        res = make_response(dumps(mongo.db.milkdata.find()))

        res.headers['Access-Control-Allow-Origin'] = '*'

        return res


@app.route('/lab_login', methods=['GET', 'POST'])

def lab_login():
    if request.method == 'POST':

        if all(x in request.form for x in ('email','pw')): 
            
            user = mongo.db.lab_users.find_one(
                    {'email': request.form['email']} )
            

            #If user didn't return as 'None' and if password matches
            try_pw = md5.md5(request.form['pw']+request.form['email']).hexdigest()

            if user and user['password'] == try_pw:

                del user['password']
                del user['_id']

                session['email'] = user
                return redirect(url_for('lab_dashboard'))

        else:
            flash('something went wrong with your submission')
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return redirect(url_for('index'))



@app.route('/app_login', methods=['POST', 'OPTIONS'])
@origin('*', headers='Content-Type')
def login():

    

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
