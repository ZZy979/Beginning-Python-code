#!/usr/bin/env python

import cgi
import sqlite3
import sys

print('Content-Type: text/html;charset=utf-8\n')

conn = sqlite3.connect('messages.db')
curs = conn.cursor()

form = cgi.FieldStorage()
id = form.getvalue('id')

print("""
<html>
  <head>
    <title>View Message</title>
  </head>
  <body>
    <h1>View Message</h1>
    """)

try:
    id = int(id)
except:
    print('Invalid message ID')
    sys.exit()

curs.execute('SELECT * FROM messages WHERE id = ?', (id,))
names = [d[0] for d in curs.description]
rows = [dict(zip(names, row)) for row in curs.fetchall()]

if not rows:
    print('Unknown message ID')
    sys.exit()

row = rows[0]

print("""
    <b>Subject:</b> {subject}<br>
    <b>Sender:</b> {sender}<br>
    <pre>{text}</pre>
    <hr>
    <a href="main.cgi">Back to the main page</a> | <a href="edit.cgi?reply_to={id}">Reply</a>
  </body>
</html>
""".format_map(row))
