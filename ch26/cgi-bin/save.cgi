#!/usr/bin/env python

import cgi
import sqlite3
import sys

print('Content-Type: text/html;charset=utf-8\n')

conn = sqlite3.connect('messages.db')
curs = conn.cursor()

form = cgi.FieldStorage()
sender = form.getvalue('sender')
subject = form.getvalue('subject')
text = form.getvalue('text').replace('\r\n', '\n')
reply_to = form.getvalue('reply_to')

if not (sender and subject and text):
    print('Please supply sender, subject, and text')
    sys.exit()

if reply_to is not None:
    query = 'INSERT INTO messages(reply_to, sender, subject, text) VALUES (?, ?, ?, ?)'
    args = int(reply_to), sender, subject, text
else:
    query = 'INSERT INTO messages(sender, subject, text) VALUES (?, ?, ?)'
    args = sender, subject, text

curs.execute(query, args)
conn.commit()

print("""
<html>
  <head>
    <title>Message Saved</title>
  </head>
  <body>
    <h1>Message Saved</h1>
    <hr>
    <a href="main.cgi">Back to the main page</a>
  </body>
</html>
""")
