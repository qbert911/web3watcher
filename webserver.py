#!/usr/bin/env python3
from flask import Flask, render_template
import epoch_log_process
import curve_log_process
app = Flask(__name__)

@app.route('/')
def index():
    z=curve_log_process.daily_log(1,1,0)
    news=curve_log_process.show_me(-1, (z*24), 0, curve_log_process.update_price(), 1000, 0, 0)
    return render_template('index.html', news=news)

@app.route('/<name>')
def hello(name):
    if name == "prospectus":
        return render_template('prospectus.html')
    else:
        invarray = epoch_log_process.load_investor_epochs(name)
        epochsdict, profitdict = epoch_log_process.find_epochs(name,0)
        return render_template('page.html', name=name, epochsdict = epochsdict, profitdict = profitdict, invarray=invarray)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='4242')
