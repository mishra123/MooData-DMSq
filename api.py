

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
	if request.method == 'POST':
		session['username'] = request.form['username']
		return redirect(url_for('index'))





if __name__ == "__main__":
    app.run(debug=True)