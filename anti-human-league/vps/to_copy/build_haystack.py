import itertools
import os
import string

for product in itertools.product(string.ascii_lowercase, repeat=3):
    dest = '/'.join(product)
    cmd = 'mkdir -p haystack/%s' % dest
    print(cmd)
    os.system(cmd)
