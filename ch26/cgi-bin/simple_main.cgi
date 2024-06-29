#!/usr/bin/env python

import cgitb
import sqlite3

print('Content-Type: text/html;charset=utf-8\n')

cgitb.enable()

conn = sqlite3.connect('messages.db')
curs = conn.cursor()

print("""
<html>
  <head>
    <title>The FooBar Bulletin Board</title>
  </head>
  <body>
    <h1>The FooBar Bulletin Board</h1>
    """)

curs.execute('SELECT * FROM messages')
names = [d[0] for d in curs.description]
rows = [dict(zip(names, row)) for row in curs.fetchall()]

toplevel = []
children = {}

for row in rows:
    parent_id = row['reply_to']
    if parent_id is None:
        toplevel.append(row)
    else:
        children.setdefault(parent_id, []).append(row)


def format(row):
    print('<p>{}</p>'.format(row['subject']))
    try:
        kids = children[row['id']]
    except KeyError:
        pass
    else:
        print('<blockquote>')
        for kid in kids:
            format(kid)
        print('</blockquote>')


for row in toplevel:
    format(row)

print("""
  </body>
</html>
""")
