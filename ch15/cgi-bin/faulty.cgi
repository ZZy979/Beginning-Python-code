#!/usr/bin/env python

import cgitb

cgitb.enable()

print('Content-Type: text/html\n')
print(1/0)
print('Hello, world!')
