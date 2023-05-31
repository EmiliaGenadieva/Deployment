import logging
from joblib import load
import urllib.request
from flask import Flask, redirect, render_template, url_for, request
import json
import plotly
import plotly.express as px
import pandas as pd
import requests
from bs4 import BeautifulSoup
from wsgiref.simple_server import WSGIServer

app = Flask(__name__)

file = 'https://firebasestorage.googleapis.com/v0/b/inappvegetarian.appspot.com/o/filename.skops?alt=media&token=787bbd34-a73f-4175-a004-5196f8698231'
clf = load(urllib.request.urlopen(file))


@app.route('/dict')
def jprint(living, bedrooms, surface):
    return json.dumps({"Living_area": living, "Bedrooms": bedrooms, "Surface_plot": surface}, sort_keys=True, indent=4)

@app.route('/home/<price>', methods = ['POST', 'GET'])
def home(price):
    if request.method == 'GET':
        return render_template('home.html', price = price)
    return render_template('home.html', price = price)

@app.route('/', methods = ['POST', 'GET'])
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

@app.route('/charts', methods = ['POST', 'GET'])
def charts():
    if request.method == 'GET':
        return render_template('charts.html')


@app.route('/chart3', methods = ['POST', 'GET'])
def chart3():
    if request.method == 'GET':
        url = 'https://www.internetlivestats.com/total-number-of-websites/'
        s = requests.Session()
        response = s.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        right_table=soup.find('table', {"class":'table table-striped table-bordered table-hover table-condensed table-list'})
        rows = right_table.findAll("tr")
        lst_data1 = []
        for row in rows:  
            data = [d.text.rstrip() for d in row.select('td')]
            lst_data1.append(data)
        lst_data1 = pd.DataFrame(lst_data1)
        df = lst_data1.copy()
        headers=df.iloc[0]
        df  = pd.DataFrame(df.values[1:], columns=headers)
        df['Websites'] = df["Websites"].str.replace(',','')
        df['Websites'] = pd.to_numeric(df['Websites'])
        fig = px.bar(df[:-1], x="Year (June)", y="Websites", barmode = 'group')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        header="Vegetables in Europe"
        description = """
        The rumor that vegetarians are having a hard time in London and Madrid can probably not be
        explained by this chart.
        """
        return render_template('chart3.html', graphJSON=graphJSON, header=header,description=description)


if __name__ == '__main__':
    app.run()
    # Production
    http_server = WSGIServer((), app)
    http_server.serve_forever()
    if app.config['LOG_WITH_GUNICORN']:
        gunicorn_error_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.DEBUG)
