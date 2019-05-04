from pwn import *

HOST = 'localhost'
PORT = 9001

tube = remote(HOST, PORT)
payload = tube.readline().strip().decode('utf-8')
tube.sendline(payload)
print(tube.readline())
