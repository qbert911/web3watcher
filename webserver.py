#!/usr/bin/env python3
from flask import Flask, render_template
import datetime
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<name>')
def hello(name):
    amount = 2000
    humantime = "2021/01/01"

    profit = 20.14
    
    y, m, d = int(humantime[0:4]), int(humantime[5:7]), int(humantime[8:10])
    timestamp = round((time.time() - datetime.datetime(y, m, d, 0, 0).timestamp()) / (60*60*24), 1)
    return render_template('page.html', name=name, timestamp=timestamp, humantime=humantime, amount=amount, profit=profit)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='4242')
