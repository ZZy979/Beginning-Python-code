#!/usr/bin/env python

import cgi

form = cgi.FieldStorage()
name = form.getvalue('name', 'world')

print('''Content-Type: text/html;charset=utf-8

<html>
  <head>
    <title>Greeting Page</title>
  </head>
  <body>
    <h1>Hello, {}!</h1>

    <form action="simple3.cgi">
    Change name <input type="text" name="name" />
    <input type="submit" />
    </form>
  </body>
</html>
'''.format(name))
