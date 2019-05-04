from interact import Bot
from PIL import Image
import base64
import pytesseract
import io
from ocr_mapper import mapper

BASE_URL = 'http://ahl.threatsims.com:5000'
VPS_URL = BASE_URL + '/vps-practice/'

bot = Bot()

def get_new_image():
    global bot, VPS_URL
    soup = bot.get(VPS_URL)
    image_data = base64.b64decode(soup.find_all('img', { 'id': 'image_captcha' })[0]['src'].split(',')[1])
    image = Image.open(io.BytesIO(image_data))

    ocrd = pytesseract.image_to_string(image)
    real = soup.find('div', { 'id': 'image_captcha_text' }).decode_contents()

    for a,b in mapper:
        ocrd = ocrd.replace(a, b)

    return ocrd, real

ocrd, real = get_new_image()
while ocrd != real:
    print('Inaccuracy found:')
    print(repr(ocrd))
    print(repr(real))
    print()
    ocrd, real = get_new_image()
else:
    soup = bot.post(VPS_URL, { 'image_captcha': ocrd })
    print(soup)
