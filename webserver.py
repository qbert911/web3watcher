#!/usr/bin/env python3
from flask import Flask, render_template
import datetime
import time
import epoch_log_process

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<name>')
def hello(name):
    humantime = "2021/01/01"
    y, m, d = int(humantime[0:4]), int(humantime[5:7]), int(humantime[8:10])
    timestamp = round((time.time() - datetime.datetime(y, m, d, 0, 0).timestamp()) / (60*60*24), 1)
    dic = { "profit": [30.14,20,13,2], "amount": 2000, "humantime":humantime, "timestamp":timestamp}
    invarray = epoch_log_process.load_investor_epochs(name)
    epochsdict, profitdict = epoch_log_process.find_epochs()
    return render_template('page.html', dic=dic, epochsdict = epochsdict, profitdict = profitdict, name=name, invarray=invarray)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='4242')
