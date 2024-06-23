#!/usr/bin/env python

import cgi

form = cgi.FieldStorage()

text = form.getvalue('text', open('simple_edit.dat').read()).replace('\r\n', '\n')
with open('simple_edit.dat', 'w') as f:
    f.write(text)

print("""Content-Type: text/html;charset=utf-8

<html>
  <head>
    <title>A Simple Editor</title>
  </head>
  <body>
    <form action='simple_edit.cgi' method='POST'>
    <textarea rows='10' cols='20' name='text'>{}</textarea><br />
    <input type='submit' />
    </form>
  </body>
</html>
""".format(text))
