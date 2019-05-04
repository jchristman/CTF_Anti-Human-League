from flask import Flask, render_template, request, redirect, make_response, g, session, render_template_string
from uuid import uuid4
import datetime
import urllib

TIMEOUT = 2

def initialize():
    session['expected_captcha'] = ''
    session['captcha_expiration'] = datetime.datetime.now() + datetime.timedelta(seconds=TIMEOUT)
    session['banned'] = False

def set_captcha(captcha):
    if not 'expected_captcha' in session:
        initialize()
    session['expected_captcha'] = captcha
    session['captcha_expiration'] = datetime.datetime.now() + datetime.timedelta(seconds=TIMEOUT)

def robotgate(request, captcha_func=lambda captcha: True, disable=False):
    if not 'expected_captcha' in session:
        initialize()

    if disable or 'static' in request.path:
        return False, ''

    if session['banned']:
        msg = urllib.parse.quote_plus('YOU HAVE BEEN FLAGGED AS A HUMAN!!! GO AWAY!!!')
        return True, redirect('/error?msg=%s' % msg)

    if session['captcha_expiration'] < datetime.datetime.now():
        session['banned'] = True
        msg = urllib.parse.quote_plus('YOU TOOK TOO LONG AND ARE THEREFORE A HUMAN!!! BANNING YOUR BROWSER!!!')
        return True, redirect('/error?msg=%s' % msg)

    result = captcha_func(request.args.get('captcha'), session['expected_captcha'])
    if result is None:
        return True, None

    if not result:
        session['banned'] = True
        msg = urllib.parse.quote_plus('CAPTCHA WAS INCORRECT AND YOU ARE THEREFORE A HUMAN!!! BANNING YOUR BROWSER!!!')
        return True, redirect('/error?msg=%s' % msg)

    return False, ''

