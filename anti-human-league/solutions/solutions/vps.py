from interact import Bot
from PIL import Image
import base64
import pytesseract
import io
from ocr_mapper import mapper
import paramiko
import time
import threading

BASE_URL = 'http://ahl.threatsims.com:5000'
VPS_URL = BASE_URL + '/vps/'

bot = Bot()

def get_new_image(soup):
    image_data = base64.b64decode(soup.find_all('img', { 'id': 'image_captcha' })[0]['src'].split(',')[1])
    image = Image.open(io.BytesIO(image_data))

    ocrd = pytesseract.image_to_string(image)

    for a,b in mapper:
        ocrd = ocrd.replace(a, b)

    return ocrd

soup = bot.get(VPS_URL)
ocrd = get_new_image(soup)

found_ssh = False
ssh_line = ''
password = ''
while True:
    for p in soup.find_all('p'):
        tmp = p.decode_contents()
        if 'successfully submitted' in tmp:
            print(tmp)
        elif 'ssh' in tmp:
            ssh_line = tmp
            found_ssh = True
        elif 'Password:' in tmp:
            password = tmp.split(': ')[1]

    if found_ssh:
        break

    soup = bot.post(VPS_URL, { 'image_captcha': ocrd })
    ocrd = get_new_image(soup)

username, hostname = ssh_line.split(' ')[1].split('@')

def keepalive(bot):
    for i in range(10):
        # Need to keep this alive since we are taking longer than two seconds
        print('keepalive')
        bot.get(VPS_URL)
        time.sleep(1.5)

threading.Thread(target=keepalive, args=(bot,)).start()

print('Connecting to %s with %s:%s' % (hostname, username, password))
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, username=username, password=password)
channel = client.invoke_shell()

stdin = channel.makefile('wb')
stdout = channel.makefile('r')

def exec(cmd):
    global stdin
    stdin.write(cmd.strip() + '\n')
    stdin.flush()

def recv():
    global stdout
    data = ''
    while not '$' in data:
        data += stdout.read(1).decode('utf-8')
    return data

recv()
print(recv())

print('[.] Hiding needle in haystack')
exec('./hide_needle')
print(recv())

print('[.] Finding pieces of the needle')
exec('find | grep "[0-9]"')
data = recv()

lines = [line for line in data.splitlines() if 'haystack' in line]
files = sorted(lines, key=lambda x: int(x.split('/')[-1]))
print(files)

cmd = 'cat %s' % ' '.join(files)

print('[.] Reassembling the key')
exec(cmd)
data = recv()
key = [line.strip() for line in data.splitlines() if '-' in line][0]

client.close()

print('[.] Posting the key to the VPS')
soup = bot.post(VPS_URL, { 'ssh_needle': key })
print(soup)
