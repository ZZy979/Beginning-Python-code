#!/usr/bin/env python

import cgi
import sys
from os.path import abspath, join

print('Content-Type: text/html;charset=utf-8\n')

BASE_DIR = abspath('data')

form = cgi.FieldStorage()
filename = form.getvalue('filename')
if not filename:
    print('Please enter a file name')
    sys.exit()
text = open(join(BASE_DIR, filename), encoding='utf-8').read()

print("""
<html>
  <head>
    <title>Editing...</title>
  </head>
  <body>
    <form action='save.cgi' method='POST'>
      <b>File:</b> {}<br />
      <input type='hidden' value='{}' name='filename' />
      <b>Password:</b><br />
      <input name='password' type='password' /><br />
      <b>Text:</b><br />
      <textarea name='text' cols='40' rows='20'>{}</textarea><br />
      <input type='submit' value='Save' />
    </form>
  </body>
</html>
""".format(filename, filename, text))
