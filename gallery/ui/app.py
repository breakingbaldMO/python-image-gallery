from flask import Flask
from flask import request
from flask import render_template
from gallery/tools/db import add_user

app = Flask(__name__)

@app.route('/admin')
def hello_world():
    return 'Welcome to the "users" database table!'

@app.route('/addUser')
def goodbye():
    return 'addUser'

@app.route('/greet/<name>')
def greet(name):
    return 'Nice to meet you ' + name

@app.route('/mult')
def mult():
    x = request.args['x']
    y = request.args['y']
    return 'the product is ' + str(int(x) * int(y))

