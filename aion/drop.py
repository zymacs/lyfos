import sqlite3

conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()

cur.execute("""
SELECT name FROM sqlite_master
WHERE type='table' AND name LIKE ?
""", ("%accounts_%",))

tables = [row[0] for row in cur.fetchall()]

for table in tables:
    cur.execute(f'DROP TABLE IF EXISTS "{table}"')

conn.commit()
conn.close()
