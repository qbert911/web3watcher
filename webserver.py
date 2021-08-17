#!/usr/bin/env python3
from flask import Flask, render_template
import json
import tools.epoch_log_process
from tools.hour_log_process import show_me, daily_log
from tools.price_getter import update_price
app = Flask(__name__)
import os

myarray = json.load(open("pyportal.json", 'r'))

@app.route('/')
def index():
    z=daily_log(1,1,0)
    news=show_me(-1, (z*24), 0, update_price("curve-dao-token"), 1000, 0, 0)
    return render_template('index.html', news=news)

@app.route('/<name>')
def hello(name):
    if name == "prospectus":
        return render_template('prospectus.html')
    elif name == "pyportal":
        return myarray
    else:
        invarray = tools.epoch_log_process.load_investor_epochs(name)
        epochsdict, profitdict = tools.epoch_log_process.find_epochs(name,0)
        return render_template('page.html', name=name, epochsdict = epochsdict, profitdict = profitdict, invarray=invarray)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='4242')
