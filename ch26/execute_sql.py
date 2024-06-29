import sqlite3
import sys

conn = sqlite3.connect(sys.argv[1])
cursor = conn.cursor()
with open(sys.argv[2], encoding='utf-8') as f:
    cursor.execute(f.read())
conn.commit()
conn.close()
