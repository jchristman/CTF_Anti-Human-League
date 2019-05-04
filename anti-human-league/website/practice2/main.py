from flask import Flask, render_template, request, redirect, make_response, g, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = '53693a98-fa49-439d-9fa0-0771b740fe66'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///practice2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'
_session = Session(app)

FLAG = 'flag{you_sur3_d0_b3h4v3_lik3_a_b0t}'

def init():
    if not 'SUCCESS_COUNT' in session:
        session['SUCCESS_COUNT'] = 0

@app.route('/')
def index():
    init()
    SUCCESS_COUNT = session['SUCCESS_COUNT']
    return render_template('anti-human-league.html', SUCCESS_COUNT=SUCCESS_COUNT, FLAG=FLAG)

def success():
    init()
    session['SUCCESS_COUNT'] += 1

@app.cli.command('initdb')
def initdb_command():
    _session.app.session_interface.db.create_all()

