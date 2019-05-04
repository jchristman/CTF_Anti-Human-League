from pwn import *

HOST = 'localhost'
PORT = 9002

tube = remote(HOST, PORT)

for i in range(100):
    print('Round %i' % i)
    payload = tube.readline().strip().decode('utf-8')
    tube.sendline(payload)

print(tube.readline())
