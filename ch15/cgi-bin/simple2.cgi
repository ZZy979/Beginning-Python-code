#!/usr/bin/env python

import cgi

form = cgi.FieldStorage()
name = form.getvalue('name', 'world')

print('Content-Type: text/plain\n')
print('Hello, {}!'.format(name))
