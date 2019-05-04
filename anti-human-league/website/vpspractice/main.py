from flask import Flask, render_template, request, redirect, make_response, g, session
import base64
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from uuid import uuid4
from flask_session import Session

app = Flask(__name__)
app.secret_key = '794e97a0-6d18-4702-8ac2-75939564e336'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vpspractice.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'
_session = Session(app)

FLAG = 'flag{oh_s33_ar3_is_hard}'

def init():
    if not 'SUCCESS_COUNT' in session:
        session['SUCCESS_COUNT'] = 0
        session['IMAGE_CAPTCHA'] = ''


@app.route('/', methods=['GET', 'POST'])
def index():
    init()
    if request.method == 'POST':
        image_captcha = request.form['image_captcha']
        if session['IMAGE_CAPTCHA'] == image_captcha:
            session['SUCCESS_COUNT'] += 1

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
                            flag=FLAG)

@app.cli.command('initdb')
def initdb_command():
    _session.app.session_interface.db.create_all()

