#!/usr/bin/env python3
import json
import logging
import click
from flask import Flask
app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass
def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass
click.echo = echo
click.secho = secho

@app.route('/')
def index():
    myarray = json.load(open("pyportal.json", 'r'))
    return myarray

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='4242')
