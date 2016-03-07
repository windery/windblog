#!venv/bin/python
#-*- coding: utf-8 -*-

from flask import Flask
from flask.ext.script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
@app.route('/index/<name>')
def index(name=None):
    if name is None:
        return '<h1>hello world!</h1>'
    else:
        return '<h1>hello %s!</h1>' % name

if __name__ == '__main__':
    manager.run()
