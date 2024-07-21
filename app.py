import logging
from joblib import load
import urllib.request
import json
import plotly
import plotly.express as px
import pandas as pd
import requests
from bs4 import BeautifulSoup
from wsgiref.simple_server import WSGIServer
from flask import Flask, redirect, render_template, url_for, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

#file = ''
#clf = load(urllib.request.urlopen(file))
price = 280000
home_page = 'home.html'

# declare the main route of the app
@app.route('/', methods = ['POST', 'GET'])
def home0():
    if request.method == 'GET':
        return render_template(home_page)     
    return render_template(home_page)

# route to print the API response of the predicted prices and their values
@app.route('/dict')
def jprint(living, bedrooms, surface):
    return json.dumps({"Living_area": living, "Bedrooms": bedrooms, "Surface_plot": surface}, sort_keys=True, indent=4)

# declare route to the result of the price
@app.route('/home/<price>', methods = ['POST', 'GET'])
def home(price):
    if request.method == 'GET':
        if price == None:
            return render_template('index.html', price = price)
        else:
            return render_template(home_page, price = price)
    return render_template(home_page, price = price)

# declare route to get values of the form to calculate the predicted price
@app.route('/index', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        salary = request.form['salary']
        tax =  request.form['tax']
        bonus =  request.form['bonus']
        record={"Living_area": salary, "Bedrooms":tax, "Surface_plot":bonus}
        jprint(salary, tax, bonus )
        #price = clf.predict([[key for key in record.values()]])
        return redirect(url_for('home', price = 'Predicted price ' + str(int(price))+ '€'))
    else:
        salary = request.args.get('salary')
        tax = request.args.get('tax')
        bonus = request.args.get('bonus')
        record = {"Living_area": salary, "Bedrooms":tax, "Surface_plot":bonus}
        return render_template('index.html', record = record)

# route to Google charts example
@app.route('/charts', methods = ['POST', 'GET'])
def charts():
    if request.method == 'GET':
        return render_template('charts.html')

# route which directs to web scraping charts example
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
        df  = pd.DataFrame(df.to_numpy()[1:], columns=headers)
        df['Websites'] = df["Websites"].str.replace(',','')
        df['Websites'] = pd.to_numeric(df['Websites'])
        fig = px.bar(df[:-1], x="Year (June)", y="Websites", barmode = 'group')
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        header="Distribution online Webpages"
        description = """
        The idea that the number of webpages is decreasing can probably not be
        explained by this chart.
        """
        return render_template('chart3.html', graphJSON=graph_json, header=header,description=description)

@app.route('/tfpredict1', methods = ['POST', 'GET'])
def tfpredict1():
    print("hello")
    return render_template('tfpredict1.html')

@app.route('/tfpredict', methods = ['POST', 'GET'])
def tfpredict():
    print("hello")
    return render_template('tfpredict.html')

@app.route('/testpredictimage', methods = ['POST', 'GET'])
def testpredictimage():
    print("hello")
    return render_template('testpredictimage.html')

@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e
    
    # now you're handling non-HTTP exceptions only
    return render_template("500_generic.html", e=e), 500

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
    # Production
    http_server = WSGIServer((), app)
    http_server.serve_forever()
    if app.config['LOG_WITH_GUNICORN']:
        gunicorn_error_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.DEBUG)
