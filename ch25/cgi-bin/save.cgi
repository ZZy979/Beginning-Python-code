#!/usr/bin/env python

import cgi
import sys
from hashlib import sha1
from os.path import abspath, join

print('Content-Type: text/html;charset=utf-8\n')

BASE_DIR = abspath('data')

form = cgi.FieldStorage()

text = form.getvalue('text').replace('\r\n', '\n')
filename = form.getvalue('filename')
password = form.getvalue('password')

if not (filename and text and password):
    print('Invalid parameters.')
    sys.exit()

if sha1(password.encode()).hexdigest() != '8843d7f92416211de9ebb963ff4ce28125932878':
    print('Invalid password')
    sys.exit()

with open(join(BASE_DIR, filename), 'w', encoding='utf-8') as f:
    f.write(text)

print('The file has been saved.')
