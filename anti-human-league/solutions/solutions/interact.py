from bs4 import BeautifulSoup
import requests
import hashlib
import json
from requests_toolbelt.utils import dump


class Bot:
    def __init__(self):
        self.session = requests.session()
        self.challenge = ''

    def solve_captcha(self):
        if 'sha1' in self.challenge:
            challenge = self.challenge.split('(')[1][:-1]
            return hashlib.sha1(bytes(challenge, 'utf-8')).hexdigest()
        return ''

    def get(self, url):
        captcha = self.solve_captcha()
        payload = { 'captcha': captcha }
        r = self.session.get(url, params=payload)
        soup = BeautifulSoup(r.text, features='html.parser')
        captcha_div = soup.find('div', { 'id': 'captcha' })
        self.challenge = captcha_div.decode_contents()
        return soup

    def post(self, url, args):
        captcha = self.solve_captcha()
        params = { 'captcha': captcha }
        r = self.session.post(url, params=params, data=args)
        soup = BeautifulSoup(r.text, features='html.parser')
        try:
            captcha_div = soup.find('div', { 'id': 'captcha' })
        except:
            print(soup)
            print('------ No Captcha to Find ------')
            return soup
        self.challenge = captcha_div.decode_contents()
        return soup
