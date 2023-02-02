from joblib import load
import urllib.request
from flask import Flask, redirect, render_template, url_for, request
import json


app = Flask(__name__)
app.secret_key = ''
clf = load(urllib.request.urlopen("https://firebasestorage.googleapis.com/v0/b/inappvegetarian.appspot.com/o/filename.joblib?alt=media&token=2ce49114-6300-4bb8-a59d-653dc8f8bca8"))

@app.route('/dict')
def jprint(living, bedrooms, surface):
    return json.dumps({"Living_area": living, "Bedrooms": bedrooms, "Surface_plot": surface}, sort_keys=True, indent=4)

@app.route('/home/<price>', methods = ['POST', 'GET'])
def home(price):
    if request.method == 'GET':
        return render_template('home.html', price = price)

@app.route('/',methods = ['POST', 'GET'])
@app.route('/index')
def index():
    if request.method == 'POST':
        salary = request.form['salary']
        tax =  request.form['tax']
        bonus =  request.form['bonus']
        record={"Living_area": salary, "Bedrooms":tax, "Surface_plot":bonus}
        jprint(salary, tax, bonus )
        price = clf.predict([[key for key in record.values()]])
        return redirect(url_for('home', price = 'Predicted price ' + str(int(price))+ '€'))
    else:
        salary = request.args.get('salary')
        tax = request.args.get('tax')
        bonus = request.args.get('bonus')
        record = {"Living_area": salary, "Bedrooms":tax, "Surface_plot":bonus}
        return render_template('index.html', record = record)

if __name__ == '__main__':
    app.run(threaded=True)