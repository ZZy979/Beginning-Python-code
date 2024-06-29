import sqlite3

conn = sqlite3.connect('messages.db')
curs = conn.cursor()

reply_to = input('Reply to: ')
subject = input('Subject: ')
sender = input('Sender: ')
text = input('Text: ')

if reply_to:
    query = 'INSERT INTO messages(reply_to, sender, subject, text) VALUES(?, ?, ?, ?)'
    args = (reply_to, subject, sender, text)
else:
    query = 'INSERT INTO messages(sender, subject, text) VALUES (?, ?, ?)'
    args = (subject, sender, text)

curs.execute(query, args)
conn.commit()
conn.close()
