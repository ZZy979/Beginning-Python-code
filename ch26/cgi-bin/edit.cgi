#!/usr/bin/env python

import cgi
import sqlite3

print('Content-Type: text/html;charset=utf-8\n')

conn = sqlite3.connect('messages.db')
curs = conn.cursor()

form = cgi.FieldStorage()
reply_to = form.getvalue('reply_to')

print("""
<html>
  <head>
    <title>Compose Message</title>
  </head>
  <body>
    <h1>Compose Message</h1>

    <form action="save.cgi" method="POST">
    """)

subject = ''
if reply_to is not None:
    print('<input type="hidden" name="reply_to" value="{}" />'.format(reply_to))
    curs.execute('SELECT subject FROM messages WHERE id = ?', (reply_to,))
    subject = curs.fetchone()[0]
    if not subject.startswith('Re: '):
        subject = 'Re: ' + subject

print("""
      <b>Subject:</b><br>
      <input type="text" size="40" name="subject" value="{}" /><br>
      <b>Sender:</b><br>
      <input type="text" size="40" name="sender" /><br>
      <b>Message:</b><br>
      <textarea name="text" cols="40" rows="20"></textarea><br>
      <input type="submit" value="Save" />
    </form>
    <hr>
    <a href="main.cgi">Back to the main page</a>
  </body>
</html>
""".format(subject))
