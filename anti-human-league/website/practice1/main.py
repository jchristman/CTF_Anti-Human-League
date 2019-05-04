from flask import Flask, render_template, request, redirect, make_response, g, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = '44888dea-97b1-4d0b-a86b-ce3ebdd6a25e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///practice1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'
_session = Session(app)

FLAG = 'flag{r0b0ts_ar3_s0_much_b3tt3r_th4n_hum4nz}'

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
