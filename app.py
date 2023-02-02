from joblib import load
import urllib.request
from flask import Flask, redirect, render_template, url_for, request
import json
from wsgiref.simple_server import WSGIServer


app = Flask(__name__)
file = 'https://firebasestorage.googleapis.com/v0/b/proplisting-b1b6b.appspot.com/o/filename.skops?alt=media&token=657aee24-a6bf-4694-b045-59855ff0944d'
clf = load(urllib.request.urlopen(file))

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
    app.run()
    # Production
    http_server = WSGIServer((), app)
    http_server.serve_forever()
