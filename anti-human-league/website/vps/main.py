from flask import Flask, render_template, request, redirect, make_response, g, session
import base64
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from uuid import uuid4
from flask_session import Session

app = Flask(__name__)
app.secret_key = '06f5efb4-f731-49ea-a80a-4912db93db19'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vps.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'
_session = Session(app)

FLAG = 'flag{ju5t_wh4t_u_n33d3d...moar_p0w3r}'
KEY = '60a6cf0b-f534-4502-9f92-a578dcb0e679'
SECRET = 'c5368001-70a3-46b4-a2a4-da646b333a75'
PASSWORD = 'Not yet updated'
PASSWORD_FILE = 'vps-ssh-password.txt'
if os.path.isfile(PASSWORD_FILE):
    PASSWORD = open(PASSWORD_FILE).read()
else:
    with open(PASSWORD_FILE, 'w') as f:
        f.write(PASSWORD)

def init():
    if not 'SUCCESS_COUNT' in session:
        session['SUCCESS_COUNT'] = 0
        session['IMAGE_CAPTCHA'] = ''


@app.route('/new_password', methods=['GET', 'POST'])
def new_password():
    global SECRET, PASSWORD
    if request.method == 'POST':
        if request.form['secret'] == SECRET:
            with open(PASSWORD_FILE, 'w') as f:
                PASSWORD = request.form['new_password']
                f.write(PASSWORD)
            print('Updated password to',PASSWORD)
    return ''

@app.route('/', methods=['GET', 'POST'])
def index():
    global PASSWORD
    init()
    success = False
    if request.method == 'POST':
        if 'ssh_needle' in request.form:
            success = request.form['ssh_needle'] == KEY
        else:
            image_captcha = request.form['image_captcha']
            if session['IMAGE_CAPTCHA'] == image_captcha:
                session['SUCCESS_COUNT'] += 1
                if session['SUCCESS_COUNT'] == 20:
                    PASSWORD = open(PASSWORD_FILE).read()

    session['IMAGE_CAPTCHA'] = str(uuid4())

    img = Image.new('RGB', (820, 60), color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("Consolas.ttf", 40)
    d.text((15,14), session['IMAGE_CAPTCHA'], fill=(0,0,0), font=font)
    buffer = BytesIO()
    img.save(buffer, format='png')
    myimage = buffer.getvalue()
    data = 'data:image/png;base64,{}'.format(base64.b64encode(myimage).decode())

    return render_template('anti-human-league.html',
                            image_captcha=data,
                            test=session['IMAGE_CAPTCHA'],
                            success_count=session['SUCCESS_COUNT'],
                            password=PASSWORD,
                            success=success,
                            flag=FLAG)

@app.cli.command('initdb')
def initdb_command():
    _session.app.session_interface.db.create_all()

