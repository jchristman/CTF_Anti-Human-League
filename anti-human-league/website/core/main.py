from flask import Flask, render_template, request, redirect, make_response, g, session
from uuid import uuid4
from common import robotgate

app = Flask(__name__)
app.secret_key = str(uuid4())

@app.route('/')
def index():
    return render_template('anti-human-league.html')

@app.route('/error')
def error():
    msg = request.args.get('msg')
    return render_template('error.html', msg=msg)

