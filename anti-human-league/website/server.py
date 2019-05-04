#/usr/bin/env python
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask import Flask, request, g

import core
import practice1
import practice2
import blog
import vpspractice
import vps

import hashlib
from bs4 import BeautifulSoup
from common import robotgate, set_captcha
from uuid import uuid4

DEBUG = False
DISABLE_CAPTCHA = False

app = DispatcherMiddleware(core.app, {
    '/practice1': practice1.app,
    '/practice2': practice2.app,
    '/blog': blog.app,
    '/vps-practice': vpspractice.app,
    '/vps': vps.app
})

_apps = [
    (blog.app, None),
    (practice1.app, practice1.success),
    (practice2.app, practice2.success),
    (vpspractice.app, None),
    (vps.app, None)
]

def gen_captcha():
    to_hash = str(uuid4())
    _hash = hashlib.sha1(to_hash.encode('ascii')).hexdigest()
    return _hash, to_hash

def captcha_func(guess, expected):
    if DISABLE_CAPTCHA:
        return True
    if expected == '':
        return None
    return guess == expected

def make_before_request(_app, _success):
    @_app.before_request
    def before_request():
        failed, redirect = robotgate(request, captcha_func, DISABLE_CAPTCHA)
        if failed:
            if redirect is None:  # This happens with empty captcha first time visiting page
                return
            return redirect

        if not _success is None:
            _success()

    return before_request

def make_after_response(_app, _success):
    @_app.after_request
    def after_response(response):
        if response.status_code == 200:
            captcha_solution, captcha = gen_captcha()
            set_captcha(captcha_solution)

            try:
                data = response.response[0]
                soup = BeautifulSoup(data, features='html.parser')
                center_tag = soup.new_tag('center', style='position: fixed; bottom: 5px; width: 100%')
                captcha_tag = soup.new_tag('div', id='captcha')
                captcha_tag.string = 'sha1(%s)' % captcha
                center_tag.append(captcha_tag)
                soup.body.append(center_tag)
                data = soup.encode(formatter='html5')
                response.set_data(data)
            except:
                pass

        return response

    return after_response

for _app, _success in _apps:
    make_before_request(_app, _success)
    make_after_response(_app, _success)


if __name__ == '__main__':
    run_simple('0.0.0.0', 5000, app, use_reloader=DEBUG, use_debugger=DEBUG)
